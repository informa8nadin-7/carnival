"""Тесты для логики команды `/plus1` (без Telegram/aiogram)."""

from __future__ import annotations

import pytest

from src.bot.services.plus3 import build_plus1_response


@pytest.mark.parametrize(
    "text, expected_answer",
    [
        (None, "Не вижу команду целиком. Напиши так: /plus1 10"),
        ("/plus1", "Напиши число после команды. Например: /plus1 10"),
        ("/plus1   ", "Напиши число после команды. Например: /plus1 10"),
        ("/plus1 котик", "Это не похоже на целое число. Пример: /plus1 10"),
        ("/plus1 10", "10 + 1 = 11"),
        ("/plus1 -5", "-5 + 1 = -4"),
        ("/plus1 0007", "7 + 1 = 8"),
    ],
)
def test_handle_plus1_answers_expected(text: str | None, expected_answer: str) -> None:
    """Логика должна выдавать понятный ответ для разных входов."""
    assert build_plus1_response(text) == expected_answer

