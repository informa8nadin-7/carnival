"""Бизнес-логика для команды `/plus1` (без зависимостей от aiogram).

Идея простая: на вход приходит текст сообщения (или None),
на выход — готовый текст ответа для пользователя.
"""

from __future__ import annotations

from .math import add_one


def build_plus1_response(message_text: str | None) -> str:
    """Строит ответ для команды `/plus1`.

    Args:
        message_text: Полный текст сообщения, например `"/plus1 10"`.

    Returns:
        Текст, который нужно отправить пользователю.
    """
    if not message_text:
        return "Не вижу команду целиком. Напиши так: /plus1 10"

    parts = message_text.split(maxsplit=1)
    if len(parts) < 2:
        return "Напиши число после команды. Например: /plus1 10"

    raw_value = parts[1].strip()
    try:
        value = int(raw_value)
    except ValueError:
        return "Это не похоже на целое число. Пример: /plus1 10"

    result = add_one(value)
    return f"{value} + 1 = {result}"

