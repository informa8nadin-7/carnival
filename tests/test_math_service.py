"""Тесты для функций сервисного слоя `math`."""

import pytest

from src.bot.services.math import add_three


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, 3),
        (10, 13),
        (-5, -2),
    ],
)
def test_add_three(value: int, expected: int) -> None:
    """Проверяем, что число увеличивается ровно на 3."""
    assert add_three(value) == expected

