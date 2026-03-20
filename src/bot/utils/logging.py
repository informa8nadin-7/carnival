"""Настройка логирования приложения."""

import logging
import os
from logging import Logger


def setup_logging() -> Logger:
    """Настраивает базовое логирование и возвращает логгер приложения.

    Логгер пишет сообщения в стандартный вывод.
    Уровень логирования можно задать через переменную окружения LOG_LEVEL
    (например, DEBUG, INFO, WARNING, ERROR). По умолчанию INFO.
    """
    log_level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_name, logging.INFO)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    logger = logging.getLogger("bot")
    logger.info("Уровень логирования установлен на %s", log_level_name)
    return logger

