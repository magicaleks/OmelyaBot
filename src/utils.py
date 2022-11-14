from .db.database import db
from .replies import replies
from .misc.keyboards import signup_kb
import aiogram

async def check_user(id: int) -> bool:
    user = await db.get_user(id)
    if not user or (user and not user.phone):
        bot = aiogram.Bot.get_current()
        await bot.send_message(id, replies['start']['signup'], reply_markup=signup_kb())
        return False
    return True
