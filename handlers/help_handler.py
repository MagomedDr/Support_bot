from aiogram import Router
from aiogram.filters import Command
from states.BotStates import BotStates
from aiogram.types import Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from resources.texts import HELP_HANDLER
from aiogram import Bot
from filters.isUser import IsUserFilter
from database.db import connect_to_db
from resources.config import ADMIN_GROUP
from filters.isAdmin import IsAdminFilter
import random

router = Router()

@router.message(Command(commands=["help"]), IsUserFilter())
async def help_handler(message: Message, state: FSMContext):
    await state.set_state(BotStates.help)

    kb = [
        [KeyboardButton(text='Написать администратору')],
        [KeyboardButton(text='Назад')],
    ]
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    await message.answer(HELP_HANDLER, reply_markup=reply_keyboard)

@router.message(BotStates.help, lambda message: message.text == "Написать администратору", IsUserFilter())
async def question_handler(message: Message, state: FSMContext):
    await state.set_state(BotStates.write_to_admin)
    await message.answer("Введите ваше сообщение:")

async def write_to_db(message: Message, question_id: int, username):
    conn = await connect_to_db()
    try:
        await conn.execute("INSERT INTO question (text, user_id, question_id, username) VALUES ($1, $2, $3, $4)",
                           message.text, message.from_user.id, question_id, username)
    finally:
        await conn.close()

async def write_to_admin(message: Message, state: FSMContext, bot: Bot):
    question_id = random.randint(10000000, 99999999)
    user = await bot.get_chat(message.from_user.id)
    if user.username:
        username = f"@{user.username}"
    else:
        username = ""
    await write_to_db(message, question_id, username)

    text = f"Новый вопрос: {question_id}\nОт: {username}\nВопрос: {message.text}"
    await bot.send_message(chat_id=ADMIN_GROUP, text=text)

    await message.answer("Сообщение отправлено!")
    from handlers.back_handler import back_to_start_handler
    await back_to_start_handler(message, state)

async def forward_admin_response(message: Message, bot: Bot):
    conn = await connect_to_db()
    try:
        question_parts = message.text.split(" ")
        if len(question_parts) >= 3:
            question_id = int(question_parts[1])
            answer_text = " ".join(question_parts[2:])

            async with conn.transaction():
                user_id = await conn.fetchval("SELECT user_id FROM question WHERE question_id = $1", question_id)

                if user_id:
                    await bot.send_message(user_id, f"Ответ на ваш вопрос:\n{answer_text}")
                    await conn.execute("DELETE FROM question WHERE question_id = $1", question_id)
                    await message.answer("Ваш ответ отправлен.")
                else:
                    await message.answer("Не удалось найти вопрос с указанным идентификатором.")
        else:
            await message.answer("Чтобы ответить, введите команду в формате:\n/answer <id_вопроса> <ответ>")
    
    finally:
        await conn.close()


async def get_next_questions(offset):
    conn = await connect_to_db()
    try:
        questions = await conn.fetch("SELECT * FROM question LIMIT 5 OFFSET $1", offset)
        return questions
    finally:
        await conn.close()

@router.message(Command(commands=["questions"]), IsAdminFilter())
async def send_questions(message: Message, state: FSMContext, offset = 0):
    await state.set_state(BotStates.questions)
    questions = await get_next_questions(offset)
    if questions:
        response = "Список вопросов:\n\n"
        for question in questions:
            response += f"ID: {question['question_id']}\nОт: {question['username']}\nВопрос: {question['text']}\n\n"

        remaining_questions = await get_next_questions(offset + 5)
        if remaining_questions:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Загрузить ещё 5", callback_data=f"load_more_{offset+5}")]
                ]
            )
            await message.answer(response, reply_markup=keyboard)
        else:
            await message.answer(response)
    else:
        await message.answer("Нет вопросов.")

@router.callback_query(BotStates.questions, lambda callback_query: True)
async def load_more_questions_callback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    offset = int(callback_query.data.split("_")[2])
    await send_questions(callback_query.message, state, offset)
