#!/usr/bin/env python3
"""
Точка входа для запуска Telegram-бота на Amvera.

Этот файл используется Amvera для запуска приложения.
Он запускает бота в режиме long-polling.
"""

import sys
import os

# Добавляем путь к src для корректного импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.bot.main import run_bot

if __name__ == "__main__":
    print("Запуск Telegram-бота через long-polling...")
    run_bot()