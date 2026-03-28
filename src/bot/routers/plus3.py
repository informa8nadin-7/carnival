"""Обработчик команды /plus1.

Команда принимает число и возвращает число + 1.
Пример: /plus1 10 -> 11
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from ..services.plus3 import build_plus1_response


plus1_router = Router()


@plus1_router.message(Command("plus1"))
async def handle_plus1(message: Message) -> None:
    """Обрабатывает команду /plus1 и увеличивает число на 1."""
    await message.answer(build_plus1_response(message.text))

