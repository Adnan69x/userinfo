import logging
import asyncio
from telethon import TelegramClient, events
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    try:
        client = TelegramClient('bot_session', config.API_ID, config.API_HASH)
        await client.start(bot_token=config.BOT_TOKEN)
        logger.info("Bot has been started successfully.")

        @client.on(events.NewMessage(pattern=r'/info (\@\w+)'))
        async def handler(event):
            try:
                username = event.pattern_match.group(1)  # Extract the username from the command
                if username:
                    user = await client.get_entity(username)
                    user_full_name = f"{user.first_name} {user.last_name}".strip()
                    response_message = (
                        f"<b>User ID:</b> {user.id}\n"
                        f"<b>Full Name:</b> {user_full_name}\n"
                        f"<b>Username:</b> @{user.username if user.username else 'No username'}"
                    )
                    await event.respond(response_message)
                    logger.info(f"Provided info for username {user.username}.")
                else:
                    await event.respond("Please provide a valid username after the /info command.")
                    logger.error("No username provided.")
            except ValueError:
                await event.respond("Please provide a valid username after the /info command.")
                logger.error("Invalid username provided.")
            except Exception as e:
                await event.respond("An error occurred while processing your request.")
                logger.error(f"Error retrieving user info: {str(e)}")

        await client.run_until_disconnected()
    except Exception as e:
        logger.error(f"Error starting the bot: {str(e)}")

if __name__ == '__main__':
    asyncio.run(main())