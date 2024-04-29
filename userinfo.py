from aiogram import Bot, Dispatcher, types, executor
import datetime
from config import API_TOKEN

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Function to handle user info request
@dp.message_handler(commands=['info'])
async def userinfo(message: types.Message):
    # Extract user information from the message object
    user = message.from_user

    # Simulated client data (as an example, this would not be actual data from Telegram)
    user_client = "Simulated: Telegram iOS"

    # Provide user info, excluding the account creation date
    await message.reply(f"User ID: {user.id}\n"
                        f"Full Name: {user.full_name}\n"
                        f"Username: {user.username}\n"
                        f"Client: {user_client}")

# Start the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
