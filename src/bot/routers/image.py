"""Роутер для команды /image — генерация изображений с помощью AI."""

import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import asyncio

from ..services.image_generation import generate_image

logger = logging.getLogger(__name__)

image_router = Router()


@image_router.message(Command("image"))
async def handle_image_command(message: Message, state: FSMContext) -> None:
    """Обрабатывает команду /image <описание> — генерирует изображение."""
    logger.info("Команда /image получена от пользователя %s", message.from_user.id)

    # Извлекаем описание из текста команды
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer(
            "Пожалуйста, укажите описание изображения после команды.\n"
            "Пример: `/image кот в шляпе`"
        )
        return

    prompt = parts[1].strip()
    if not prompt:
        await message.answer("Описание не может быть пустым.")
        return

    # Показываем индикатор "печатает"
    await message.bot.send_chat_action(chat_id=message.chat.id, action="upload_photo")

    # Индикатор "печатает..." с периодическим обновлением
    async def typing_indicator():
        while True:
            await message.bot.send_chat_action(chat_id=message.chat.id, action="upload_photo")
            await asyncio.sleep(5)  # Telegram обновляет индикатор каждые 5 секунд

    typing_task = asyncio.create_task(typing_indicator())
    try:
        # Генерируем изображение
        image_url = await generate_image(prompt)
    except Exception as e:
        logger.error("Ошибка при генерации изображения: %s", e)
        await message.answer(
            "Произошла ошибка при генерации изображения. "
            "Проверьте, задан ли API-ключ Polza.ai и поддерживает ли он генерацию изображений."
        )
        return
    finally:
        typing_task.cancel()
        try:
            await typing_task
        except asyncio.CancelledError:
            pass

    if image_url is None:
        await message.answer(
            "Не удалось сгенерировать изображение. "
            "Убедитесь, что API-ключ Polza.ai задан и модель поддерживает генерацию изображений."
        )
        return

    # Отправляем изображение как фото
    try:
        await message.answer_photo(image_url, caption=f"Сгенерировано по запросу: {prompt}")
        logger.info("Изображение отправлено пользователю %s", message.from_user.id)
    except Exception as e:
        logger.error("Ошибка при отправке изображения: %s", e)
        await message.answer(f"Изображение сгенерировано, но не удалось отправить. URL: {image_url}")