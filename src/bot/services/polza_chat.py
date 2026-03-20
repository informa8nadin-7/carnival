"""Сервис для взаимодействия с Polza.ai через HTTP POST (стандартная библиотека)."""

import json
import logging
from typing import List, Dict, Any
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from ..config import load_config

logger = logging.getLogger(__name__)


def _make_polza_request(messages: List[Dict[str, str]]) -> str:
    """Отправляет запрос к Polza.ai и возвращает ответ.

    Args:
        messages: Список сообщений в формате OpenAI, например:
            [{"role": "user", "content": "Привет"}]

    Returns:
        Текст ответа от ИИ.

    Raises:
        RuntimeError: Если произошла ошибка при запросе.
    """
    config = load_config()

    if not config.polza_api_key:
        logger.warning("Polza.ai API key not set, using demo response.")
        return "Это демо-ответ, потому что API-ключ Polza.ai не задан. Добавьте POLZA_API_KEY в .env файл."

    url = f"{config.polza_base_url}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config.polza_api_key}",
    }
    payload = {
        "model": config.polza_model,
        "messages": messages,
        "max_tokens": 500,
        "temperature": 0.7,
    }

    logger.info("Отправка запроса к Polza.ai: URL=%s, модель=%s, количество сообщений=%d",
                url, config.polza_model, len(messages))
    logger.debug("Заголовки: %s", {k: v if k != "Authorization" else "Bearer ***" for k, v in headers.items()})
    logger.debug("Тело запроса: %s", json.dumps(payload, ensure_ascii=False))

    try:
        request = Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        with urlopen(request, timeout=30) as response:
            response_body = response.read().decode("utf-8")
            logger.debug("Ответ от Polza.ai: %s", response_body)
            response_data = json.loads(response_body)
            # Извлекаем текст ответа
            if "choices" not in response_data or not response_data["choices"]:
                raise RuntimeError("Некорректный ответ от Polza.ai: отсутствует choices")
            message = response_data["choices"][0].get("message", {})
            content = message.get("content", "")
            if not content:
                raise RuntimeError("Пустой ответ от Polza.ai")
            logger.info("Успешный ответ от Polza.ai, длина: %d", len(content))
            return content.strip()
    except HTTPError as e:
        error_body = e.read().decode("utf-8") if hasattr(e, 'read') else str(e)
        logger.error("HTTP error %d from Polza.ai: %s", e.code, error_body)
        raise RuntimeError(f"Ошибка HTTP {e.code} от Polza.ai: {error_body}")
    except URLError as e:
        logger.error("URL error from Polza.ai: %s", e.reason)
        raise RuntimeError(f"Ошибка соединения с Polza.ai: {e.reason}")
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        logger.error("Parsing error from Polza.ai response: %s", e)
        raise RuntimeError("Некорректный формат ответа от Polza.ai")
    except Exception as e:
        logger.exception("Unexpected error while calling Polza.ai")
        raise RuntimeError(f"Неожиданная ошибка: {e}")


async def ask_polza(messages: List[Dict[str, str]]) -> str:
    """Асинхронная обёртка над синхронным запросом.

    В aiogram хендлеры асинхронные, но urllib синхронный.
    Чтобы не блокировать event loop, можно вынести в thread pool.
    Для простоты используем синхронный вызов, т.к. запросы не частые.
    """
    # В реальном приложении стоит использовать aiohttp, но по условию — стандартная библиотека.
    # Используем синхронный вызов в отдельном потоке через asyncio.to_thread.
    import asyncio
    return await asyncio.to_thread(_make_polza_request, messages)