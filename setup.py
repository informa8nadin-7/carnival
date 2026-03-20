#!/usr/bin/env python3
"""
Мастер настройки Telegram-бота.

Помогает создать файл .env, ввести токен бота и запустить бота.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from typing import Optional

# Цвета для консоли (опционально)
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False
    # Заглушки
    class Fore:
        GREEN = ''
        YELLOW = ''
        RED = ''
        CYAN = ''
        RESET = ''
    class Style:
        BRIGHT = ''
        RESET_ALL = ''


def print_color(text: str, color: str = Fore.GREEN, style: str = Style.RESET_ALL) -> None:
    """Печатает цветной текст, если colorama доступен."""
    if HAS_COLORAMA:
        print(f"{style}{color}{text}{Style.RESET_ALL}")
    else:
        print(text)


def read_input(prompt: str, default: Optional[str] = None) -> str:
    """Читает ввод пользователя с подсказкой."""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    try:
        value = input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print_color("\nПрервано пользователем.", Fore.RED)
        sys.exit(1)
    if not value and default is not None:
        return default
    return value


def yes_no(prompt: str, default: bool = True) -> bool:
    """Задаёт вопрос да/нет."""
    choices = "Y/n" if default else "y/N"
    full_prompt = f"{prompt} ({choices})? "
    answer = read_input(full_prompt, "").lower().strip()
    if not answer:
        return default
    return answer in ("y", "yes", "да", "д")


def check_dependencies():
    """Проверяет наличие обязательных зависимостей и предлагает установить."""
    required = ["aiogram", "dotenv"]
    missing = []
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if not missing:
        return True
    
    print_color("Обнаружены отсутствующие зависимости:", Fore.YELLOW)
    for pkg in missing:
        print_color(f"  - {pkg}", Fore.RED)
    
    if yes_no("Установить недостающие зависимости", default=True):
        print_color("Устанавливаю зависимости из requirements.txt...", Fore.CYAN)
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print_color("Зависимости успешно установлены.", Fore.GREEN)
            return True
        except subprocess.CalledProcessError as e:
            print_color(f"Ошибка установки: {e}", Fore.RED)
            if yes_no("Продолжить без зависимостей (бот может не запуститься)", default=False):
                return True
            else:
                sys.exit(1)
    else:
        print_color("Зависимости не установлены. Бот может не запуститься.", Fore.YELLOW)
        return False


def ensure_env_file() -> Path:
    """Проверяет наличие .env, создаёт из .env.example при необходимости."""
    env_path = Path(".env")
    example_path = Path(".env.example")

    if env_path.exists():
        print_color(f"Файл {env_path} уже существует.", Fore.YELLOW)
        return env_path

    print_color("Файл .env не найден.", Fore.YELLOW)
    if example_path.exists():
        print_color(f"Создаю {env_path} на основе {example_path}...", Fore.CYAN)
        shutil.copy(example_path, env_path)
    else:
        print_color(f"Создаю пустой {env_path}...", Fore.CYAN)
        env_path.touch()

    return env_path


def read_current_token(env_path: Path) -> Optional[str]:
    """Читает текущий токен из .env файла."""
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("BOT_TOKEN="):
                    return line.split("=", 1)[1].strip()
    except FileNotFoundError:
        pass
    return None


def write_token_to_env(env_path: Path, token: str) -> None:
    """Записывает токен в .env файл, заменяя существующую строку BOT_TOKEN."""
    lines = []
    token_written = False
    token_line = f"BOT_TOKEN={token}\n"

    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("BOT_TOKEN="):
                    lines.append(token_line)
                    token_written = True
                else:
                    lines.append(line)
    if not token_written:
        lines.append(token_line)

    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print_color(f"Токен сохранён в {env_path}", Fore.GREEN)


def validate_token(token: str) -> bool:
    """Проверяет, что токен выглядит как Telegram Bot Token."""
    # Простая проверка формата: число:буквенно-цифровой_символы
    if ":" not in token:
        return False
    parts = token.split(":", 1)
    if not parts[0].isdigit():
        return False
    if len(parts[1]) < 10:
        return False
    return True


def main():
    """Основная функция мастера."""
    print_color("=== Мастер настройки Telegram-бота ===", Fore.CYAN, Style.BRIGHT)
    print()

    # 0. Проверяем зависимости
    check_dependencies()
    print()

    # 1. Убедимся, что .env существует
    env_path = ensure_env_file()

    # 2. Прочитаем текущий токен
    current_token = read_current_token(env_path)
    if current_token:
        print_color(f"Текущий токен: {current_token[:10]}...", Fore.YELLOW)
        change = yes_no("Хотите изменить токен", default=False)
        if not change:
            token = current_token
        else:
            token = None
    else:
        token = None

    # 3. Запросим новый токен, если нужно
    if token is None:
        print_color("Введите токен вашего бота, полученный от @BotFather.", Fore.CYAN)
        print_color("Пример: 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz", Fore.CYAN)
        while True:
            token = read_input("BOT_TOKEN", "").strip()
            if not token:
                print_color("Токен не может быть пустым.", Fore.RED)
                continue
            if not validate_token(token):
                print_color("Токен выглядит некорректно. Проверьте формат.", Fore.RED)
                if not yes_no("Всё равно продолжить", default=False):
                    continue
            break
        write_token_to_env(env_path, token)
    else:
        print_color("Токен остаётся без изменений.", Fore.GREEN)

    # 4. Предложим запустить бота
    print()
    print_color("Настройка завершена!", Fore.GREEN, Style.BRIGHT)
    if yes_no("Запустить бота сейчас", default=True):
        print_color("Запускаю бота...", Fore.CYAN)
        os.system("python -m src.bot")
    else:
        print_color("Вы можете запустить бота вручную командой:", Fore.CYAN)
        print_color("  python -m src.bot", Fore.CYAN)
        print_color("Спасибо за использование мастера!", Fore.GREEN)


if __name__ == "__main__":
    main()