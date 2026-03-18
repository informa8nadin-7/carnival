"""Тесты для функций сервисного слоя `text`."""

import pytest

from src.bot.services.text import build_welcome_text, build_help_text, build_echo_text


def test_build_welcome_text_uses_name() -> None:
    """Проверяем, что имя пользователя попадает в приветствие."""
    text = build_welcome_text("Алиса")
    assert "Алиса" in text


def test_build_welcome_text_uses_default_when_empty() -> None:
    """Если имя пустое, используется слово 'друг'."""
    text = build_welcome_text("  ")
    assert "друг" in text


def test_build_help_text_non_empty() -> None:
    """Текст помощи не должен быть пустым."""
    text = build_help_text()
    assert isinstance(text, str)
    assert text.strip() != ""


@pytest.mark.parametrize(
    "user_text, expected",
    [
        ("привет", "привет"),
        ("  пробелы вокруг  ", "пробелы вокруг"),
    ],
)
def test_build_echo_text_returns_clean_text(user_text: str, expected: str) -> None:
    """Проверяем, что эхо-функция очищает лишние пробелы."""
    assert build_echo_text(user_text) == expected


def test_build_echo_text_handles_empty() -> None:
    """Если текст пустой, возвращается понятное сообщение."""
    text = build_echo_text("   ")
    assert "ничего не написал" in text

