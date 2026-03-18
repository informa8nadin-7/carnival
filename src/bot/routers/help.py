"""Обработчик команды /help."""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from ..services.text import build_help_text


help_router = Router()


@help_router.message(Command("help"))
async def handle_help(message: Message) -> None:
    """Отправляет пользователю подсказку по использованию бота."""
    help_text = build_help_text()
    await message.answer(help_text)

