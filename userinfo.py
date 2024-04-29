from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import logging
from config import API_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['info'])
async def user_info(message: types.Message):
    # Extract the mentioned username from the command
    target_username = message.get_args()
    
    if not target_username:
        await message.reply("Please specify a username after the command.")
        return
    
    if message.chat.type == "private":
        # If the command is sent in a private chat, retrieve the information of the user who sent the command
        user = message.from_user
        user_id = user.id
        full_name = user.full_name
        username = user.username
    else:
        # If the command is sent in a group, check if the mentioned user is the same as the user who sent the command
        mentioned_user = await bot.get_chat(target_username)
        if mentioned_user.id == message.from_user.id:
            user = message.from_user
        else:
            user = mentioned_user
        
        user_id = user.id
        full_name = user.full_name
        username = user.username
    
    await message.reply(
        f"ID: {user_id}\n"
        f"Full Name: {full_name}\n"
        f"Username: {username}"
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)