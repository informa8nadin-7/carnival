"""Тесты для функций сервисного слоя `text`."""

import pytest

from src.bot.services.text import (
    build_welcome_text,
    build_help_text,
    build_echo_text,
    build_plain_text_reply,
)


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


@pytest.mark.parametrize(
    "user_text, expected",
    [
        ("10", "11"),
        ("  0  ", "1"),
        ("-1", "0"),
        ("0007", "8"),
    ],
)
def test_build_plain_text_reply_increments_integers(
    user_text: str, expected: str
) -> None:
    """Если пользователь прислал целое число, бот отвечает числом + 1."""
    assert build_plain_text_reply(user_text) == expected


@pytest.mark.parametrize(
    "user_text, expected",
    [
        ("привет", "привет"),
        ("  текст  ", "текст"),
        ("", "Ты ничего не написал, поэтому мне нечего повторять 🙂"),
        ("   ", "Ты ничего не написал, поэтому мне нечего повторять 🙂"),
    ],
)
def test_build_plain_text_reply_falls_back_to_echo(
    user_text: str, expected: str
) -> None:
    """Если это не число, используется обычное эхо-поведение."""
    assert build_plain_text_reply(user_text) == expected

