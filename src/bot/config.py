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
    polza_api_key: str
    polza_model: str
    polza_base_url: str
    polza_history_messages_limit: int


def load_config() -> BotConfig:
    """Загружает конфигурацию из `.env` и переменных окружения.

    Возвращает объект `BotConfig` с токеном бота и настройками Polza.ai.
    """
    # Загружаем переменные окружения из файла .env, если он существует
    if ENV_PATH.is_file():
        load_dotenv(dotenv_path=ENV_PATH)

    bot_token = os.getenv("BOT_TOKEN")
    polza_api_key = os.getenv("POLZA_API_KEY", "")
    polza_model = os.getenv("POLZA_MODEL", "gpt-3.5-turbo")
    polza_base_url = os.getenv("POLZA_BASE_URL", "https://api.polza.ai/v1")
    polza_history_messages_limit = int(os.getenv("POLZA_HISTORY_MESSAGES_LIMIT", "5"))

    if not bot_token:
        # Явная ошибка, чтобы быстро понять проблему с конфигурацией
        raise RuntimeError("Переменная окружения BOT_TOKEN не задана")

    return BotConfig(
        bot_token=bot_token,
        polza_api_key=polza_api_key,
        polza_model=polza_model,
        polza_base_url=polza_base_url,
        polza_history_messages_limit=polza_history_messages_limit,
    )
