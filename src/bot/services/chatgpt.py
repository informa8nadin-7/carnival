"""Сервис для взаимодействия с Polza.ai (OpenAI-compatible API)."""

import os
import logging
from typing import List, Dict, Any

try:
    from openai import AsyncOpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    logging.warning("openai library not installed, ChatGPT functionality will be disabled.")

logger = logging.getLogger(__name__)

# Конфигурация Polza.ai
POLZAAI_API_KEY = os.getenv("pza_rRfY1JQNSHHUzMTP24vxbAMkWDtlhjF8", "")
POLZAAI_BASE_URL = os.getenv("POLZAAI_BASE_URL", "https://api.polza.ai/v1")

# Если ключ не задан, можно использовать демо-режим (не рекомендуется для продакшена)
DEMO_MODE = not POLZAAI_API_KEY

if HAS_OPENAI and not DEMO_MODE:
    client = AsyncOpenAI(
        api_key=POLZAAI_API_KEY,
        base_url=POLZAAI_BASE_URL,
    )
else:
    client = None


async def ask_chatgpt(messages: List[Dict[str, str]]) -> str:
    """Отправляет запрос к Polza.ai и возвращает ответ.

    Args:
        messages: Список сообщений в формате OpenAI, например:
            [{"role": "user", "content": "Привет"}]

    Returns:
        Текст ответа от ИИ.

    Raises:
        Exception: Если произошла ошибка при запросе.
    """
    if DEMO_MODE:
        logger.warning("Polza.ai API key not set, using demo response.")
        return "Это демо-ответ, потому что API-ключ Polza.ai не задан. Добавьте POLZAAI_API_KEY в .env файл."

    if not HAS_OPENAI:
        return "Библиотека openai не установлена. Установите её: pip install openai."

    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",  # или другая модель, поддерживаемая Polza.ai
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.exception("Ошибка при запросе к Polza.ai")
        raise RuntimeError(f"Ошибка API Polza.ai: {e}")