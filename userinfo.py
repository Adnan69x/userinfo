from aiogram import Bot, Dispatcher, types, executor
from config import API_TOKEN

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Function to handle user info request with a username parameter
@dp.message_handler(commands=['info'])
async def userinfo(message: types.Message):
    # Extract the parameter from the message (assuming the command is formatted as /info username)
    try:
        # Split message text to get username parameter
        command, username_param = message.text.split(maxsplit=1)
    except ValueError:
        # In case no parameter was provided
        await message.reply("Please provide a username with the command. Example: /info yourusername")
        return

    # Check if the provided username matches the sender's username
    if message.from_user.username == username_param:
        # User information to be provided
        user = message.from_user

        # Provide user info
        await message.reply(f"User ID: {user.id}\n"
                            f"Full Name: {user.full_name}\n"
                            f"Username: {user.username}")
    else:
        # If usernames do not match, you might choose not to reply or to send a different message
        await message.reply("No information available.")

# Start the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
