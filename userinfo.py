import logging
from telethon import TelegramClient, events
import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Telegram Client
client = TelegramClient('bot_session', config.API_ID, config.API_HASH)

async def main():
    await client.start(bot_token=config.BOT_TOKEN)
    logger.info("Bot has been started successfully.")

    @client.on(events.NewMessage(pattern=r'/info (\@\w+)'))
    async def handler(event):
        # Check if the message is from a group or channel
        if event.is_group or event.is_channel:
            group_id = event.chat_id
            group_error = False
        else:
            group_id = None
            group_error = True

        username = event.pattern_match.group(1)  # Extract the username from the command
        if username:
            try:
                user = await client.get_entity(username)
                user_full_name = f"{user.first_name} {user.last_name if user.last_name else ''}".strip()
                user_id = user.id
                username = user.username
                response_message = (
                    f"User ID: {user_id}\n"
                    f"Full Name: {user_full_name}\n"
                    f"Username: @{username if username else 'No username'}"
                )
                if group_id:  # Include group ID if available
                    response_message += f"\nGroup ID: {group_id}"
                await event.respond(response_message)
                logger.info(f"Provided info for username {username}.")
            except ValueError:
                # ValueError occurs when the user is not found
                if not group_error:
                    await event.respond("User not found.")
                logger.error("User not found.")
            except Exception as e:
                if not group_error:
                    await event.respond("Failed to retrieve information for the given username.")
                logger.error(f"Error retrieving user info: {str(e)}")
        else:
            await event.respond("Please provide a valid username after the /info command.")

    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())
