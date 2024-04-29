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

    @client.on(events.NewMessage(pattern=r'/info'))
    async def handler(event):
        if event.is_group:
            try:
                await event.respond("Gathering group member information...")
                all_participants = await client.get_participants(event.chat_id)

                for user in all_participants:
                    user_info = (
                        f"ID: {user.id}\n"
                        f"Name: {user.first_name} {user.last_name if user.last_name else ''}\n"
                        f"Username: @{user.username if user.username else 'No username'}\n"
                        f"Situation: {user.status.__class__.__name__}\n"
                        f"Join: {user.date if user.date else 'Unknown'}\n"
                        f"Messages: {user.participant.messages if hasattr(user, 'participant') else 'N/A'}\n"
                        f"Last Message: {user.status.was_online if hasattr(user.status, 'was_online') else 'Unknown'}\n"
                    )
                    await event.respond(user_info)

            except Exception as e:
                await event.respond("Failed to retrieve group information.")
                logger.error(f"Error retrieving group info: {str(e)}")

        elif event.is_private:
            user = await event.get_sender()
            group_id = event.chat_id if event.is_group else "Private chat"
            last_update = user.status
            last_update_desc = f'{last_update.__class__.__name__} at {last_update.was_online if hasattr(last_update, "was_online") else "N/A"}' if last_update else 'N/A'

            personal_info = (
                f"User ID: {user.id}\n"
                f"Full Name: {user.first_name} {user.last_name if user.last_name else ''}\n"
                f"Group ID: {group_id}\n"
                f"Last update: {last_update_desc}"
            )
            await event.respond(personal_info)
            logger.info(f"Provided personal info for user {user.id}.")

    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())
