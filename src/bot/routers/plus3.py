"""Обработчик команды /plus3.

Команда принимает число и возвращает число + 3.
Пример: /plus3 10 -> 13
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from ..services.math import add_three


plus3_router = Router()


@plus3_router.message(Command("plus3"))
async def handle_plus3(message: Message) -> None:
    """Обрабатывает команду /plus3 и увеличивает число на 3."""
    if not message.text:
        await message.answer("Не вижу команду целиком. Напиши так: /plus3 10")
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Напиши число после команды. Например: /plus3 10")
        return

    raw_value = parts[1].strip()
    try:
        value = int(raw_value)
    except ValueError:
        await message.answer("Это не похоже на целое число. Пример: /plus3 10")
        return

    result = add_three(value)
    await message.answer(f"{value} + 3 = {result}")

