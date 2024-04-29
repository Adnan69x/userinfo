from aiogram import Bot, Dispatcher, types, executor
from config import API_TOKEN

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# In-memory storage for user data
user_data = {}

# Handler to store user data
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user = message.from_user
    user_data[user.username] = {
        'id': user.id,
        'full_name': user.full_name,
        'username': user.username
    }
    await message.reply("You are now registered. Use /info <username> to get info.")

# Function to handle user info request with a username parameter
@dp.message_handler(commands=['info'])
async def userinfo(message: types.Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) == 2:
        _, username_param = parts
        if username_param in user_data:
            user = user_data[username_param]
            await message.reply(f"User ID: {user['id']}\n"
                                f"Full Name: {user['full_name']}\n"
                                f"Username: {user['username']}")
        else:
            # Provide a more detailed explanation why the info is not available
            await message.reply(f"No information available for the provided username '{username_param}'. "
                                "The user must interact with the bot by sending /start before their information can be accessed.")
    else:
        await message.reply("Please provide a username with the command. Example: /info yourusername")

# Start the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
