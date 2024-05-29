from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


userKB = [
    [
        KeyboardButton(text='Заказы'), 
        KeyboardButton(text='Новости')
    ],
    [KeyboardButton(text='Помощь')],
]
userKeyboard = ReplyKeyboardMarkup(
    keyboard=userKB,
    resize_keyboard=True,
)

adminKB = [
    [KeyboardButton(text='Вопросы')],
    [KeyboardButton(text='Добавить новость')],
]
adminKeyboard = ReplyKeyboardMarkup(
    keyboard=adminKB,
    resize_keyboard=True,
)