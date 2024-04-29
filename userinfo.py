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

    # Placeholder for client data retrieval logic
    # For demonstration, let's assume it's a static string
    user_client = "Telegram iOS"  # Replace this with your method to get the actual client info

    # Calculate approximate account creation date from user ID
    created_at = datetime.datetime.utcfromtimestamp((int(user.id) >> 22) + 1288834974657) / 1000.0

    # Provide user info
    await message.reply(f"User ID: {user.id}\n"
                        f"Full Name: {user.full_name}\n"
                        f"Username: {user.username}\n"
                        f"Client: {user_client}\n"
                        f"Account Created: {created_at.strftime('%Y-%m-%d %H:%M:%S')}")

# Start the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
