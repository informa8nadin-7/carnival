"""Простые клавиатуры для бота."""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Создаёт простую клавиатуру с основными командами.

    Клавиатура помогает пользователю быстро вызывать команды.
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/start"), KeyboardButton(text="/help")],
            [KeyboardButton(text="/echo привет")],
            [KeyboardButton(text="/plus3 10")],
            [KeyboardButton(text="/plus3_input"), KeyboardButton(text="/cancel")],
            [KeyboardButton(text="/echo_off"), KeyboardButton(text="/echo_on")],
            [KeyboardButton(text="/chatgpt"), KeyboardButton(text="/chatgpt_off")],
        ],
        resize_keyboard=True,
    )
