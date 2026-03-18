"""Обработчик команды /plus3.

Команда принимает число и возвращает число + 3.
Пример: /plus3 10 -> 13
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from ..services.plus3 import build_plus3_response


plus3_router = Router()


@plus3_router.message(Command("plus3"))
async def handle_plus3(message: Message) -> None:
    """Обрабатывает команду /plus3 и увеличивает число на 3."""
    await message.answer(build_plus3_response(message.text))

