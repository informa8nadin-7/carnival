"""Диалоговый режим: ввёл число -> получил число + 3.

Команда:
- /plus3_input — бот попросит ввести число
- /cancel — отмена режима ввода числа
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from ..services.math import add_three


class Plus3InputStates(StatesGroup):
    """Состояния для диалога ввода числа."""

    waiting_for_number = State()


plus3_input_router = Router()


@plus3_input_router.message(Command("plus3_input"))
async def handle_plus3_input_start(message: Message, state: FSMContext) -> None:
    """Стартуем диалог: просим пользователя ввести число."""
    await state.set_state(Plus3InputStates.waiting_for_number)
    await message.answer("Введи целое число, а я прибавлю к нему 3. (Отмена: /cancel)")


@plus3_input_router.message(Command("cancel"))
async def handle_cancel(message: Message, state: FSMContext) -> None:
    """Отменяет любой диалоговый режим."""
    await state.clear()
    await message.answer("Ок, отменил. Можешь писать дальше.")


@plus3_input_router.message(Plus3InputStates.waiting_for_number, F.text)
async def handle_plus3_input_number(message: Message, state: FSMContext) -> None:
    """Принимаем число и отвечаем числом + 3."""
    raw = (message.text or "").strip()
    try:
        value = int(raw)
    except ValueError:
        await message.answer("Это не целое число. Попробуй ещё раз или нажми /cancel.")
        return

    result = add_three(value)
    await state.clear()
    await message.answer(f"{value} + 3 = {result}")

