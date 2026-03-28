"""Роутер для команды /translate — перевод текста на английский."""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import logging

from ..services.translation import translate_to_english

logger = logging.getLogger(__name__)

translate_router = Router()


class TranslateStates(StatesGroup):
    """Состояния для режима перевода."""
    waiting_for_text = State()


@translate_router.message(Command("translate"))
async def handle_translate_command(message: Message, state: FSMContext) -> None:
    """Обрабатывает команду /translate — входит в режим перевода."""
    logger.info("Команда /translate получена от пользователя %s", message.from_user.id)
    # Проверяем, есть ли текст после команды
    command_text = message.text.strip()
    parts = command_text.split(maxsplit=1)
    if len(parts) > 1:
        # Пользователь сразу написал текст для перевода
        text_to_translate = parts[1]
        await process_translation(message, text_to_translate)
        return

    # Если текст не указан, переводим в состояние ожидания
    await state.set_state(TranslateStates.waiting_for_text)
    await message.answer(
        "Отправьте текст, который нужно перевести на английский язык.\n"
        "Для отмены используйте команду /cancel."
    )


@translate_router.message(StateFilter(TranslateStates.waiting_for_text), F.text & ~F.text.startswith("/"))
async def handle_text_for_translation(message: Message, state: FSMContext) -> None:
    """Обрабатывает текст для перевода в состоянии ожидания."""
    text = message.text.strip()
    if not text:
        await message.answer("Пожалуйста, отправьте непустой текст.")
        return

    await process_translation(message, text)
    # Очищаем состояние после перевода
    await state.clear()


@translate_router.message(StateFilter(TranslateStates.waiting_for_text))
async def handle_non_text_in_translate(message: Message) -> None:
    """Обрабатывает не текстовые сообщения в режиме перевода."""
    await message.answer("Пожалуйста, отправьте текст для перевода. Для отмены используйте /cancel.")


async def process_translation(message: Message, text: str) -> None:
    """Выполняет перевод и отправляет результат."""
    logger.info("Перевод текста от пользователя %s: %s", message.from_user.id, text[:100])
    # Показываем индикатор "печатает"
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    # Выполняем перевод
    translation = await translate_to_english(text)
    # Отправляем результат
    await message.answer(f"Перевод на английский:\n{translation}")
    logger.info("Перевод отправлен пользователю %s", message.from_user.id)