"""Загрузка конфигурации приложения из переменных окружения."""

from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
import os


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"


@dataclass(frozen=True)
class BotConfig:
    """Настройки Telegram-бота."""

    bot_token: str


def load_config() -> BotConfig:
    """Загружает конфигурацию из `.env` и переменных окружения.

    Возвращает объект `BotConfig` с токеном бота.
    """
    # Загружаем переменные окружения из файла .env, если он существует
    if ENV_PATH.is_file():
        load_dotenv(dotenv_path=ENV_PATH)

    bot_token = os.getenv("BOT_TOKEN")

    if not bot_token:
        # Явная ошибка, чтобы быстро понять проблему с конфигурацией
        raise RuntimeError("Переменная окружения BOT_TOKEN не задана")

    return BotConfig(bot_token=bot_token)

