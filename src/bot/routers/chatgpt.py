"""Роутер для команды /chatgpt — диалог с ИИ через Polza.ai."""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from collections import deque
import logging
import asyncio

from ..config import load_config
from ..services.polza_chat import ask_polza

logger = logging.getLogger(__name__)

chatgpt_router = Router()

# Ключ для хранения контекста в FSM
CHATGPT_CONTEXT_KEY = "chatgpt_context"


class ChatGPTStates(StatesGroup):
    """Состояния для режима ChatGPT."""
    active = State()


def get_context_from_state(data: dict) -> deque:
    """Извлекает контекст из данных состояния или создаёт новый."""
    context = data.get(CHATGPT_CONTEXT_KEY)
    if context is None:
        config = load_config()
        return deque(maxlen=config.polza_history_messages_limit)
    # Контекст хранится как список, преобразуем обратно в deque
    config = load_config()
    return deque(context, maxlen=config.polza_history_messages_limit)


def save_context_to_state(context: deque, state: FSMContext) -> None:
    """Сохраняет контекст в состояние (как список)."""
    import asyncio
    asyncio.create_task(
        state.update_data({CHATGPT_CONTEXT_KEY: list(context)})
    )


@chatgpt_router.message(Command("chatgpt"))
async def handle_chatgpt_command(message: Message, state: FSMContext) -> None:
    """Обрабатывает команду /chatgpt — входит в режим диалога."""
    logger.info("Команда /chatgpt получена от пользователя %s", message.from_user.id)
    try:
        config = load_config()
        logger.info("polza_api_key: %s", "задан" if config.polza_api_key else "не задан")
        if not config.polza_api_key:
            logger.warning("POLZA_API_KEY отсутствует, отправляем сообщение об ошибке")
            await message.answer(
                "Режим ChatGPT недоступен, потому что не задан API-ключ Polza.ai.\n"
                "Добавьте POLZA_API_KEY в .env файл."
            )
            return

        await state.set_state(ChatGPTStates.active)
        # Инициализируем пустой контекст
        await state.update_data({CHATGPT_CONTEXT_KEY: []})
        current_state = await state.get_state()
        logger.info("Пользователь %s переведён в состояние ChatGPTStates.active, текущее состояние: %s",
                    message.from_user.id, current_state)
        reply_text = (
            "Вы вошли в режим диалога с ChatGPT. Отправляйте сообщения, и я буду отвечать.\n"
            "Для выхода из режима используйте команду /chatgpt_off."
        )
        await message.answer(reply_text)
        logger.info("Приветственное сообщение отправлено пользователю %s", message.from_user.id)
    except Exception as e:
        logger.exception("Ошибка в обработчике /chatgpt: %s", e)
        await message.answer("Произошла внутренняя ошибка при обработке команды.")


@chatgpt_router.message(Command("chatgpt_off"))
async def handle_chatgpt_off_command(message: Message, state: FSMContext) -> None:
    """Выход из режима диалога."""
    await state.clear()
    await message.answer("Режим диалога завершён. Возвращайтесь снова по команде /chatgpt.")


@chatgpt_router.message(StateFilter(ChatGPTStates.active), F.text & ~F.text.startswith("/"))
async def handle_dialog_message(message: Message, state: FSMContext) -> None:
    """Обрабатывает текстовые сообщения в режиме диалога."""
    logger.info("Получено текстовое сообщение в режиме ChatGPT от пользователя %s: %s",
                message.from_user.id, message.text[:50])
    user_text = message.text.strip()
    if not user_text:
        await message.answer("Пожалуйста, отправьте текст.")
        return

    # Получаем контекст
    data = await state.get_data()
    context = get_context_from_state(data)
    logger.info("Текущий размер контекста: %d", len(context))

    # Добавляем сообщение пользователя в контекст
    context.append({"role": "user", "content": user_text})

    # Немедленно показываем индикатор "печатает"
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    # Индикатор "печатает..." с периодическим обновлением
    async def typing_indicator():
        while True:
            await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
            await asyncio.sleep(5)  # Telegram обновляет индикатор каждые 5 секунд

    typing_task = asyncio.create_task(typing_indicator())
    try:
        # Запрашиваем ответ у Polza.ai
        reply = await ask_polza(list(context))
        logger.info("Получен ответ от Polza.ai, длина: %d", len(reply))
    except Exception as e:
        logger.error("Ошибка при запросе к Polza.ai: %s", e)
        await message.answer("Произошла ошибка при обращении к ИИ. Попробуйте позже.")
        return
    finally:
        typing_task.cancel()
        try:
            await typing_task
        except asyncio.CancelledError:
            pass

    # Добавляем ответ ассистента в контекст
    context.append({"role": "assistant", "content": reply})

    # Сохраняем обновлённый контекст
    save_context_to_state(context, state)

    # Отправляем ответ
    await message.answer(reply)
    logger.info("Ответ отправлен пользователю %s", message.from_user.id)


@chatgpt_router.message(StateFilter(ChatGPTStates.active))
async def handle_non_text_in_dialog(message: Message) -> None:
    """Обрабатывает не текстовые сообщения в режиме диалога."""
    await message.answer("В режиме диалога я понимаю только текст. Используйте команду /chatgpt_off для выхода.")