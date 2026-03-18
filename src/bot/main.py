"""Единственная точка инициализации и запуска бота (polling)."""

import asyncio

from .config import load_config
from .routers import get_root_router
from .utils.logging import setup_logging


def run_bot() -> None:
    """Синхронная точка входа для запуска бота.

    Оборачивает асинхронный запуск в `asyncio.run`, чтобы код было
    удобно вызывать из `__main__.py` и других мест.
    """
    asyncio.run(_run_polling())


async def _run_polling() -> None:
    """Асинхронная функция, которая настраивает и запускает бота."""
    # Импорты aiogram держим внутри функции.
    # Так юнит-тесты могут импортировать модуль `main` без установки/импорта aiogram.
    from aiogram import Bot, Dispatcher
    from aiogram.client.default import DefaultBotProperties
    from aiogram.enums import ParseMode
    from aiogram.fsm.storage.memory import MemoryStorage

    logger = setup_logging()
    config = load_config()

    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Подключаем все роутеры
    dp.include_router(get_root_router())

    logger.info("Бот запускается (long polling)...")
    try:
        await dp.start_polling(bot)
    finally:
        # Корректно закрываем сессию бота
        await bot.session.close()
        logger.info("Бот остановлен")

