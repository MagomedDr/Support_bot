import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
ADMIN_GROUP = os.getenv("ADMIN_GROUP")

PASSWORD=os.getenv("PASSWORD")
DATABASE=os.getenv("DATABASE")
HOST=os.getenv("HOST")
PORT=os.getenv("PORT")
