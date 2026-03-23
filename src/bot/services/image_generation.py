"""Сервис для генерации изображений через Polza.ai (OpenAI-compatible API)."""

import logging
from typing import Optional

try:
    from openai import AsyncOpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    logging.warning("openai library not installed, image generation will be disabled.")

from ..config import load_config

logger = logging.getLogger(__name__)


async def generate_image(prompt: str, model: str = "gpt-image-1") -> Optional[str]:
    """Генерирует изображение по текстовому описанию.

    Args:
        prompt: Текстовое описание изображения.
        model: Модель для генерации (по умолчанию "gpt-image-1").

    Returns:
        URL сгенерированного изображения или None в случае ошибки.
    """
    config = load_config()

    if not config.polza_api_key:
        logger.warning("Polza.ai API key not set, image generation unavailable.")
        return None

    if not HAS_OPENAI:
        logger.warning("OpenAI library not installed, image generation unavailable.")
        return None

    client = AsyncOpenAI(
        api_key=config.polza_api_key,
        base_url=config.polza_base_url,
    )

    try:
        response = await client.images.generate(
            model=model,
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="high",
            response_format="url",
        )
        image_url = response.data[0].url
        logger.info("Изображение успешно сгенерировано, URL: %s", image_url)
        return image_url
    except Exception as e:
        logger.exception("Ошибка при генерации изображения через Polza.ai: %s", e)
        # Попробуем использовать альтернативный endpoint через v2, если v1 не работает
        # Но для простоты просто пробросим ошибку
        raise RuntimeError(f"Ошибка генерации изображения: {e}")