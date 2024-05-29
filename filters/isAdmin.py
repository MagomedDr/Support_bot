from aiogram.types import Message
from aiogram.filters import BaseFilter
from resources.config import ADMIN_GROUP

class IsAdminFilter(BaseFilter):
    
    def __init__(self) -> None:
        self.admin_group = int(ADMIN_GROUP)
        
    async def __call__(self, message: Message) -> bool:
        cid = message.chat.id
        return cid == self.admin_group
