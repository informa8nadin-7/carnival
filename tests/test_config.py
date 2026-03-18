"""Тесты для загрузки конфигурации (`src.bot.config`)."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.bot import config as config_module


def test_load_config_raises_when_token_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    """Если BOT_TOKEN не задан, должна быть понятная ошибка."""
    monkeypatch.delenv("BOT_TOKEN", raising=False)
    # Подменяем путь к .env на несуществующий, чтобы тест не зависел от файла разработчика.
    monkeypatch.setattr(config_module, "ENV_PATH", Path("definitely-missing.env"))

    with pytest.raises(RuntimeError, match="BOT_TOKEN"):
        config_module.load_config()


def test_load_config_reads_token_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Если BOT_TOKEN задан в окружении, он попадает в BotConfig."""
    monkeypatch.setenv("BOT_TOKEN", "token-from-env")
    monkeypatch.setattr(config_module, "ENV_PATH", Path("definitely-missing.env"))

    cfg = config_module.load_config()
    assert cfg.bot_token == "token-from-env"


def test_load_config_reads_token_from_dotenv_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Если есть .env-файл, токен читается из него.

    Важно: тест не трогает реальный `.env` в проекте — используем временный файл.
    """
    dotenv_path = tmp_path / ".env"
    dotenv_path.write_text("BOT_TOKEN=token-from-file\n", encoding="utf-8")

    monkeypatch.delenv("BOT_TOKEN", raising=False)
    monkeypatch.setattr(config_module, "ENV_PATH", dotenv_path)

    cfg = config_module.load_config()
    assert cfg.bot_token == "token-from-file"

