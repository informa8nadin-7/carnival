"""Эхо-обработчик всех текстовых сообщений."""

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import F

from ..services.text import build_echo_text, build_plain_text_reply
from .chatgpt import ChatGPTStates


echo_router = Router()

ECHO_ENABLED_KEY = "echo_enabled"


class EchoStates(StatesGroup):
    """Состояния для режима эхо.

    Здесь мы не храним сложный диалог, а просто используем данные FSM,
    чтобы помнить: включено эхо или нет.
    """

    idle = State()


@echo_router.message(Command("echo"))
async def handle_echo_command(message: Message) -> None:
    """Обрабатывает команду /echo, повторяя текст после команды.

    Пример: `/echo привет` -> бот ответит `привет`.
    """
    # Убираем саму команду и пробел после неё
    text_without_command = message.text.split(maxsplit=1)
    user_text = text_without_command[1] if len(text_without_command) > 1 else ""
    reply_text = build_echo_text(user_text)
    await message.answer(reply_text)


@echo_router.message(Command("echo_off"))
async def handle_echo_off(message: Message, state: FSMContext) -> None:
    """Выключает эхо для обычных сообщений."""
    await state.update_data({ECHO_ENABLED_KEY: False})
    await message.answer("Эхо выключено. Включить обратно: /echo_on")


@echo_router.message(Command("echo_on"))
async def handle_echo_on(message: Message, state: FSMContext) -> None:
    """Включает эхо для обычных сообщений."""
    await state.update_data({ECHO_ENABLED_KEY: True})
    await message.answer("Эхо включено. Выключить: /echo_off")


@echo_router.message(F.text & ~F.text.startswith("/"))
async def handle_plain_text(message: Message, state: FSMContext) -> None:
    """Обрабатывает обычные текстовые сообщения.

    Если пользователь прислал целое число — бот отвечает числом + 1.
    В остальных случаях — повторяет текст (эхо).
    """
    import logging
    logger = logging.getLogger(__name__)
    # Если активен режим ChatGPT, не отвечаем эхом
    current_state = await state.get_state()
    logger.info("echo_router: текущее состояние = %s, ожидаемое = %s",
                current_state, ChatGPTStates.active.state)
    if current_state == ChatGPTStates.active.state:
        logger.info("Состояние активного ChatGPT, пропускаем эхо.")
        return

    data = await state.get_data()
    echo_enabled = data.get(ECHO_ENABLED_KEY, True)
    if not echo_enabled:
        await message.answer("Эхо сейчас выключено. Включить: /echo_on")
        return
    reply_text = build_plain_text_reply(message.text or "")
    await message.answer(reply_text)
