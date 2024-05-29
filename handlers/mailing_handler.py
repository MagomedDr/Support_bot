from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from states.BotStates import BotStates
from filters.isUser import IsUserFilter
from filters.isAdmin import IsAdminFilter
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from database.db import connect_to_db

router = Router()

async def is_user_subscribed(chat_id):
    conn = await connect_to_db()
    try:
        result = await conn.fetchrow("SELECT * FROM subscribe_user WHERE chat_id = $1", chat_id)
        return result is not None
    finally:
        await conn.close()

@router.message(Command(commands=["news"]), IsUserFilter())
async def news_handler(message: Message, state: FSMContext):
    await state.set_state(BotStates.news)
    text = ""
    is_subscribed = await is_user_subscribed(message.chat.id)

    if is_subscribed:
        text = "Отписаться"
    else:
        text = "Подписаться"

    kb = [
        [KeyboardButton(text=text)],
        [KeyboardButton(text='Назад')],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

    await message.answer("Новости", reply_markup=keyboard)

@router.message(lambda message: message.text == "Добавить новость", IsAdminFilter())
async def news_text(message: Message, state: FSMContext):
    await state.set_state(BotStates.news_text)
    await message.answer("Введите текст:")

async def send_message_to_subscribers(message: Message, state: FSMContext,bot: Bot):
    await state.set_state(BotStates.start)
    conn = await connect_to_db()
    try:
        subscribers = await conn.fetch("SELECT chat_id FROM subscribe_user")
        for subscriber in subscribers:
            user_id = subscriber['chat_id']
            await bot.send_message(user_id, f'Уведомление:\n{message.text}')
        await message.answer("Вы успешно отправили сообщение!")
    finally:
        await conn.close()

@router.message(BotStates.news, lambda message: message.text == "Подписаться", IsUserFilter())
async def subscribe(message: Message, state: FSMContext):
    conn = await connect_to_db()
    try:
        await conn.execute("INSERT INTO subscribe_user (chat_id) VALUES ($1)", message.chat.id)
        await message.answer("Вы успешно подписались на рассылку!")
        from handlers.back_handler import back_to_start_handler
        await back_to_start_handler(message, state)
    finally:
        await conn.close()

@router.message(BotStates.news, lambda message: message.text == "Отписаться", IsUserFilter())
async def unsubscribe(message: Message, state: FSMContext):
    conn = await connect_to_db()
    try:
        await conn.execute("DELETE FROM subscribe_user WHERE chat_id = $1", message.chat.id)
        await message.answer("Вы успешно отписались от рассылки!")
        from handlers.back_handler import back_to_start_handler
        await back_to_start_handler(message, state)
    finally:
        await conn.close()
