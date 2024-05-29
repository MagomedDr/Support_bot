from aiogram import Router
from states.BotStates import BotStates
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from filters.isAdmin import IsAdminFilter
from filters.isUser import IsUserFilter
from resources.config import ADMIN_GROUP
from handlers.help_handler import help_handler
from handlers.help_handler import send_questions
from handlers.order_handler import order_handler
from handlers.mailing_handler import news_handler
from resources.keyboards import adminKeyboard, userKeyboard

router = Router()

@router.message(lambda message: message.text in ['Назад'])
async def back_to_start_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state in [BotStates.news, BotStates.help, BotStates.write_to_admin, BotStates.order]:
        await state.set_state(BotStates.start)
        
        if message.chat.id == int(ADMIN_GROUP):
            await message.answer(text="Выберите действие:", reply_markup=adminKeyboard)
        else:
            await message.answer(text="Выберите действие:", reply_markup=userKeyboard)

@router.message(IsUserFilter(), lambda message: message.text in ['Заказы', 'Новости', 'Помощь'])
async def user_keyboard_buttons(message: Message, state: FSMContext):
    if message.text == 'Заказы':
        await order_handler(message, state)
    elif message.text == 'Новости':
        await news_handler(message, state)
    elif message.text == 'Помощь':
        await help_handler(message, state)

@router.message(IsAdminFilter(), lambda message: message.text in ['Вопросы'])
async def admin_keyboard_buttons(message: Message, state: FSMContext):
    if message.text == 'Вопросы':
        await send_questions(message, state)