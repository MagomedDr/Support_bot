import asyncpg
from resources.config import PASSWORD, DATABASE, HOST, PORT

async def connect_to_db():
    return await asyncpg.connect(
        user="bot_user",
        password=PASSWORD,
        database=DATABASE,
        host=HOST,
        port=PORT
    )
