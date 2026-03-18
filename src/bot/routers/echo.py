"""Эхо-обработчик всех текстовых сообщений."""

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import F

from ..services.text import build_echo_text


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
    """Повторяет любое текстовое сообщение пользователя.

    Это классический "эхо"-бот.
    """
    data = await state.get_data()
    echo_enabled = data.get(ECHO_ENABLED_KEY, True)
    if not echo_enabled:
        await message.answer("Эхо сейчас выключено. Включить: /echo_on")
        return

    reply_text = build_echo_text(message.text or "")
    await message.answer(reply_text)

