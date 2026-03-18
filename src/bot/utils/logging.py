"""Настройка логирования приложения."""

import logging
from logging import Logger


def setup_logging() -> Logger:
    """Настраивает базовое логирование и возвращает логгер приложения.

    Логгер пишет сообщения в стандартный вывод.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    logger = logging.getLogger("bot")
    return logger

