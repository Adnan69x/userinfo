from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
import logging
from config import API_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['info'])
async def user_info(message: types.Message):
    if message.chat.type == "private":  # Check if the command is sent in a private chat
        user = message.from_user
        user_id = user.id
        full_name = user.full_name
        group_id = None
        last_name_update = user.username
        await message.reply(
            f"User ID: {user_id}\n"
            f"Full Name: {full_name}\n"
            f"Group ID: {group_id}\n"
            f"Last Username Update: {last_name_update}"
        )
    else:  # If the command is sent in a group
        target_username_or_id = message.get_args()
        if not target_username_or_id:
            await message.reply("Please specify a username or user ID.")
            return
        try:
            user = await bot.get_chat(target_username_or_id)
        except Exception as e:
            await message.reply(f"Error: {e}")
            return
        if isinstance(user, types.User):
            user_id = user.id
            full_name = user.full_name
            username = user.username
            situation = user.status
            join_date = user.joined_date
            messages_count = user.total_count
            last_message = None  # Implement this if available in the library
            client_info = message.from_user.mention()
            await message.reply(
                f"ID: {user_id}\n"
                f"Name: {full_name}\n"
                f"Username: {username}\n"
                f"Situation: {situation}\n"
                f"Join: {join_date}\n"
                f"Messages: {messages_count}\n"
                f"Last Message: {last_message}\n"
                f"Client Info: {client_info}"
            )
        else:
            await message.reply("User not found.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)