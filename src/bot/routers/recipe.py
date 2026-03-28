"""Роутер для команды /recipe — генерация рецепта из списка продуктов."""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import logging

from ..services.recipe import generate_recipe

logger = logging.getLogger(__name__)

recipe_router = Router()


class RecipeStates(StatesGroup):
    """Состояния для режима генерации рецепта."""
    waiting_for_ingredients = State()


@recipe_router.message(Command("recipe"))
async def handle_recipe_command(message: Message, state: FSMContext) -> None:
    """Обрабатывает команду /recipe — входит в режим генерации рецепта."""
    logger.info("Команда /recipe получена от пользователя %s", message.from_user.id)
    # Проверяем, есть ли текст после команды
    command_text = message.text.strip()
    parts = command_text.split(maxsplit=1)
    if len(parts) > 1:
        # Пользователь сразу написал продукты
        ingredients = parts[1]
        await process_recipe(message, ingredients)
        return

    # Если продукты не указаны, переводим в состояние ожидания
    await state.set_state(RecipeStates.waiting_for_ingredients)
    await message.answer(
        "Перечислите продукты, которые у вас есть (через запятую или списком).\n"
        "Например: картофель, лук, яйца, сыр\n"
        "Для отмены используйте команду /cancel."
    )


@recipe_router.message(StateFilter(RecipeStates.waiting_for_ingredients), F.text & ~F.text.startswith("/"))
async def handle_ingredients_for_recipe(message: Message, state: FSMContext) -> None:
    """Обрабатывает список продуктов в состоянии ожидания."""
    ingredients = message.text.strip()
    if not ingredients:
        await message.answer("Пожалуйста, отправьте непустой список продуктов.")
        return

    await process_recipe(message, ingredients)
    # Очищаем состояние после генерации рецепта
    await state.clear()


@recipe_router.message(StateFilter(RecipeStates.waiting_for_ingredients))
async def handle_non_text_in_recipe(message: Message) -> None:
    """Обрабатывает не текстовые сообщения в режиме рецепта."""
    await message.answer("Пожалуйста, отправьте текстовый список продуктов. Для отмены используйте /cancel.")


async def process_recipe(message: Message, ingredients: str) -> None:
    """Выполняет генерацию рецепта и отправляет результат."""
    logger.info("Генерация рецепта для пользователя %s: %s", message.from_user.id, ingredients[:100])
    # Показываем индикатор "печатает"
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    # Генерируем рецепт
    recipe = await generate_recipe(ingredients)
    # Отправляем результат
    await message.answer(f"Вот рецепт, который можно приготовить из ваших продуктов:\n\n{recipe}")
    logger.info("Рецепт отправлен пользователю %s", message.from_user.id)