import asyncio
from aiogram import Dispatcher, Bot, F
from states.BotStates import BotStates
from aiogram.types import ContentType
from aiogram.filters import Command
from filters.isAdmin import IsAdminFilter
from filters.isUser import IsUserFilter
from resources.config import TOKEN
from handlers import (
    start_handler,
    back_handler,
    help_handler,
    order_handler,
    mailing_handler
)

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.message.register(help_handler.write_to_admin, BotStates.write_to_admin, lambda message: message.text not in ["Назад", "/start", "/help", "/order", "Написать администратору"], F.content_type == ContentType.TEXT, IsUserFilter())
    dp.message.register(help_handler.forward_admin_response, Command(commands=["answer"]), IsAdminFilter())
    dp.message.register(mailing_handler.send_message_to_subscribers, BotStates.news_text, lambda message: message.text not in ["Назад", "/start", "Добавить новость", "Вопросы"], F.content_type == ContentType.TEXT, IsAdminFilter())
    dp.include_routers(
            *[
                start_handler.router,
                back_handler.router,
                help_handler.router,
                order_handler.router,
                mailing_handler.router
            ]
        )
    await dp.start_polling(bot, 
                            skip_updates=True,
                        )

if __name__ == "__main__":
    asyncio.run(main())