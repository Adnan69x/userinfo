from aiogram import Bot, Dispatcher, types
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
        last_name_update = user.username
        await message.reply(
            f"User ID: {user_id}\n"
            f"Full Name: {full_name}\n"
            f"Last Username Update: {last_name_update}"
        )
    else:  # If the command is sent in a group
        target_username_or_id = message.get_args()
        if not target_username_or_id:
            await message.reply("Please specify a username or user ID.")
            return
        try:
            user_id = None
            username = None
            user_mention = None
            # Check if the argument is a username
            if target_username_or_id.startswith('@'):
                # Get the mentioned user
                mentioned_user = await bot.get_chat(target_username_or_id)
                if isinstance(mentioned_user, types.User):
                    user_id = mentioned_user.id
                    username = mentioned_user.username
                    user_mention = mentioned_user.mention()
            else:
                # Get the user based on ID
                user = await bot.get_chat(target_username_or_id)
                if isinstance(user, types.User):
                    user_id = user.id
                    username = user.username
                    user_mention = user.mention()

            if user_id:
                full_name = user.full_name
                situation = user.status
                join_date = user.joined_date
                messages_count = user.total_count
                last_message = None  # Implement this if available in the library
                await message.reply(
                    f"ID: {user_id}\n"
                    f"Name: {full_name}\n"
                    f"Username: {username}\n"
                    f"Situation: {situation}\n"
                    f"Join: {join_date}\n"
                    f"Messages: {messages_count}\n"
                    f"Last Message: {last_message}\n"
                    f"Mention: {user_mention}"
                )
            else:
                await message.reply("User not found.")

        except Exception as e:
            await message.reply(f"Error: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)