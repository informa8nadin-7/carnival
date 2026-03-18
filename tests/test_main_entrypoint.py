"""Тесты для точки запуска (`src.bot.main`)."""

from __future__ import annotations

import asyncio

import pytest

from src.bot import main as main_module


def test_run_bot_calls_asyncio_run(monkeypatch: pytest.MonkeyPatch) -> None:
    """`run_bot()` должен запускать внутреннюю корутину через `asyncio.run`."""

    called: dict[str, object] = {}

    def fake_run(coro: object) -> None:  # pragma: no cover
        # В тесте нам не важно выполнять корутину — только проверить, что её передали.
        called["coro"] = coro

    monkeypatch.setattr(asyncio, "run", fake_run)

    main_module.run_bot()

    assert "coro" in called

