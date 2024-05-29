from aiogram.fsm.state import StatesGroup, State

class BotStates(StatesGroup):
    start: State = State()
    help: State = State()
    write_to_admin: State = State()
    order: State = State()
    questions: State = State()
    news: State = State()
    news_text: State = State()