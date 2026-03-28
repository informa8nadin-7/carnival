"""Сервис для перевода текста на английский язык с использованием Polza.ai."""

import logging
from typing import List, Dict

from .polza_chat import ask_polza

logger = logging.getLogger(__name__)


async def translate_to_english(text: str) -> str:
    """Переводит текст на английский язык.

    Args:
        text: Исходный текст на любом языке.

    Returns:
        Переведённый текст на английском.
    """
    if not text.strip():
        return "Текст для перевода пуст."

    # Формируем промпт для перевода
    messages: List[Dict[str, str]] = [
        {
            "role": "system",
            "content": (
                "You are a professional translator. "
                "Translate the user's text into English. "
                "Return only the translation, without any additional explanations, notes, or comments. "
                "If the text is already in English, return it unchanged."
            )
        },
        {
            "role": "user",
            "content": text
        }
    ]

    try:
        translation = await ask_polza(messages)
        # Убираем возможные лишние пробелы
        return translation.strip()
    except Exception as e:
        logger.error("Ошибка при переводе текста: %s", e)
        return f"Ошибка перевода: {e}"