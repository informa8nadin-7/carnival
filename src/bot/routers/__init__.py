"""Регистрация всех роутеров бота в одном месте."""

from aiogram import Router

from .start import start_router
from .help import help_router
from .echo import echo_router
from .plus3 import plus3_router
from .plus3_input import plus3_input_router
from .chatgpt import chatgpt_router


def get_root_router() -> Router:
    """Создаёт корневой роутер и подключает к нему остальные.

    Возвращает готовый к использованию `Router`.
    """
    root_router = Router()
    root_router.include_router(start_router)
    root_router.include_router(help_router)
    root_router.include_router(plus3_router)
    root_router.include_router(plus3_input_router)
    root_router.include_router(chatgpt_router)  # Подключаем раньше echo_router
    root_router.include_router(echo_router)
    return root_router
