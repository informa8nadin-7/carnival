"""Тесты для логики команды `/plus3` (без Telegram/aiogram)."""

from __future__ import annotations

import pytest

from src.bot.services.plus3 import build_plus3_response


@pytest.mark.parametrize(
    "text, expected_answer",
    [
        (None, "Не вижу команду целиком. Напиши так: /plus3 10"),
        ("/plus3", "Напиши число после команды. Например: /plus3 10"),
        ("/plus3   ", "Напиши число после команды. Например: /plus3 10"),
        ("/plus3 котик", "Это не похоже на целое число. Пример: /plus3 10"),
        ("/plus3 10", "10 + 3 = 13"),
        ("/plus3 -5", "-5 + 3 = -2"),
        ("/plus3 0007", "7 + 3 = 10"),
    ],
)
def test_handle_plus3_answers_expected(text: str | None, expected_answer: str) -> None:
    """Логика должна выдавать понятный ответ для разных входов."""
    assert build_plus3_response(text) == expected_answer

