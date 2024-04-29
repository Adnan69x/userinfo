import logging
import asyncio
from telethon import TelegramClient, events
import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Telegram Client
client = TelegramClient('bot_session', config.API_ID, config.API_HASH)

async def main():
    try:
        await client.start(bot_token=config.BOT_TOKEN)
        logger.info("Bot has been started successfully.")

        @client.on(events.NewMessage(pattern=r'/info (\@\w+)'))
        async def handler(event):
            username = event.pattern_match.group(1)  # Extract the username from the command
            if username:
                try:
                    user = await client.get_entity(username)
                    user_full_name = f"{user.first_name} {user.last_name if user.last_name else ''}".strip()
                    user_id = user.id
                    username = user.username
                    response_message = (
                        f"<b>User ID:</b> {user_id}\n"
                        f"<b>Full Name:</b> {user_full_name}\n"
                        f"<b>Username:</b> @{username if username else 'No username'}"
                    )
                    await event.respond(response_message)
                    logger.info(f"Provided info for username {username}.")
                except ValueError:
                    await event.respond("Please provide a valid username after the /info command.")
                    logger.error("Invalid username provided.")
                except Exception as e:
                    await event.respond("An error occurred while processing your request.")
                    logger.error(f"Error retrieving user info: {str(e)}")
            else:
                await event.respond("Please provide a valid username after the /info command.")
                logger.error("No username provided.")

        await client.run_until_disconnected()
    except Exception as e:
        logger.error(f"Error starting the bot: {str(e)}")

if __name__ == '__main__':
    asyncio.run(main())