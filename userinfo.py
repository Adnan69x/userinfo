from aiogram import Bot, Dispatcher, types, executor
import datetime
import logging
from config import API_TOKEN

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Function to handle user info request
@dp.message_handler(commands=['info'])
async def userinfo(message: types.Message):
    try:
        # Extract user information from the message object
        user = message.from_user

        # Calculate approximate account creation date from user ID
        created_at = datetime.datetime.utcfromtimestamp(((int(user.id) >> 22) + 1288834974657) / 1000)

        # Provide user info
        await message.reply(f"User ID: {user.id}\n"
                            f"Full Name: {user.full_name}\n"
                            f"Username: {user.username}\n"
                            f"Account Created: {created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        logging.error(f"Failed to process info command: {e}")
        await message.reply("Failed to retrieve information.")

# Start the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
