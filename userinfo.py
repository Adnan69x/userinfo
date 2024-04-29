import logging
from pyrogram import Client, filters
import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Pyrogram Client
app = Client("bot_session", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

@app.on_message(filters.command("info", prefixes='/') & filters.regex(r'^/info (\@\w+)'))
async def handler(client, message):
    username = message.matches[0].group(1)  # Extract the username from the command
    if username:
        try:
            user = await app.get_users(username)
            user_full_name = f"{user.first_name} {user.last_name if user.last_name else ''}".strip()
            user_id = user.id
            username = user.username
            response_message = (
                f"<b>User ID:</b> {user_id}\n"
                f"<b>Full Name:</b> {user_full_name}\n"
                f"<b>Username:</b> @{username if username else 'No username'}"
            )
            await message.reply_text(response_message)
            logger.info(f"Provided info for username {username}.")
        except Exception as e:
            await message.reply_text("Failed to retrieve information for the given username.")
            logger.error(f"Error retrieving user info: {str(e)}")
    else:
        await message.reply_text("Please provide a valid username after the /info command.")

if __name__ == '__main__':
    app.run()
