from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from states.BotStates import BotStates
from filters.isUser import IsUserFilter
from aiogram.fsm.context import FSMContext
from database.db import connect_to_db

router = Router()

@router.message(Command(commands=["order"]), IsUserFilter())
async def order_handler(message: Message, state: FSMContext):
    await state.set_state(BotStates.order)

    kb = [
        [KeyboardButton(text='Назад')],
    ]
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    await message.answer('Введите номер заказа:', reply_markup=reply_keyboard)

async def find_order_by_tracking_number(tracking_number):
    conn = await connect_to_db()
    try:
        order = await conn.fetchrow("SELECT * FROM orders WHERE tracking_number = $1", tracking_number)
        return order
    finally:
        await conn.close()

@router.message(BotStates.order, lambda message: message.text.isdigit(), IsUserFilter())
async def tracking_number_handler(message: Message):
    track_number = message.text
    order = await find_order_by_tracking_number(track_number)
    if order:
        order_info = f"Статус: {order['status']}\nЦена: {order['total_price']}\nТрек номер: {order['tracking_number']}"
        await message.answer(order_info)
    else:
        await message.answer("Заказ с таким трек номером не найден.")
