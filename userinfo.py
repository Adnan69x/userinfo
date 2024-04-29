from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import logging
from config import API_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['info'])
async def user_info(message: types.Message):
    # Get the mentioned username after the command
    mentioned_username = message.get_args()
    
    if not mentioned_username:
        await message.reply("Please specify a username after the command.")
        return
    
    # Retrieve the user object of the mentioned username
    try:
        user = await bot.get_chat_member(message.chat.id, mentioned_username)
    except Exception as e:
        await message.reply(f"Error: {e}")
        return
    
    user_id = user.user.id
    full_name = user.user.full_name
    username = user.user.username
    
    await message.reply(
        f"User ID: {user_id}\n"
        f"Full Name: {full_name}\n"
        f"Username: {username}"
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
