import logging
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantsRecent
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
                all_participants = await client.get_participants(event.chat, aggressive=True)  # aggressive=True to ensure fetching all available data

                for user in all_participants:
                    # Fetch additional fields from participant object
                    join_date = getattr(user, 'date', 'Unknown')
                    messages_count = getattr(user, 'messages', 'N/A')  # For channels where message count is available
                    last_message_date = getattr(user.status, 'was_online', 'Unknown') if user.status else 'Unknown'

                    user_info = (
                        f"ID: {user.id}\n"
                        f"Name: {user.first_name} {user.last_name if user.last_name else ''}\n"
                        f"Username: @{user.username if user.username else 'No username'}\n"
                        f"Situation: {user.status.__class__.__name__ if user.status else 'No status'}\n"
                        f"Join: {join_date}\n"
                        f"Messages: {messages_count}\n"
                        f"Last Message: {last_message_date}\n"
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
