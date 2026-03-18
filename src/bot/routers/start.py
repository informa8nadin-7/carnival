"""Обработчик команды /start."""

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from ..services.text import build_welcome_text
from ..keyboards.common import get_main_menu_keyboard


start_router = Router()


@start_router.message(CommandStart())
async def handle_start(message: Message) -> None:
    """Отправляет приветственное сообщение пользователю.

    Здесь нет бизнес-логики, только работа с Telegram.
    """
    welcome_text = build_welcome_text(user_first_name=message.from_user.first_name or "друг")
    await message.answer(welcome_text, reply_markup=get_main_menu_keyboard())

