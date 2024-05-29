from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from states.BotStates import BotStates
from aiogram.fsm.context import FSMContext
from resources.config import ADMIN_GROUP
from resources.keyboards import adminKeyboard, userKeyboard
from resources.texts import GREETINGS

router = Router()

@router.message(Command(commands=["start"]))
async def start_handler(message: Message, state: FSMContext):
    await state.set_state(BotStates.start)

    if message.chat.id == int(ADMIN_GROUP):
        await message.answer(text='Выберите действие:', reply_markup=adminKeyboard)
    else:
        await message.answer(text=GREETINGS, reply_markup=userKeyboard)