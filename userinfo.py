import logging
from telethon.sync import TelegramClient, events
import config
import sqlite3
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Telegram Client
client = TelegramClient('bot_session', config.API_ID, config.API_HASH)

# Connect to SQLite database (or create if not exists)
conn = sqlite3.connect('user_info.db')
cursor = conn.cursor()

# Create table to store user information
cursor.execute('''CREATE TABLE IF NOT EXISTS user_info (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    full_name TEXT,
                    join_date TEXT,
                    total_messages INTEGER,
                    last_message_date TEXT
                )''')
conn.commit()

async def main():
    await client.start(bot_token=config.BOT_TOKEN)
    logger.info("Bot has been started successfully.")

    @client.on(events.NewMessage(pattern=r'/info (\@\w+)'))
    async def handler(event):
        # Check if the message is from a group or channel
        if event.is_group or event.is_channel:
            group_id = event.chat_id
        else:
            await event.respond("Please use the /info command in a group.")
            return

        username = event.pattern_match.group(1)  # Extract the username from the command
        if username:
            try:
                user = await client.get_entity(username)
                user_full_name = f"{user.first_name} {user.last_name if user.last_name else ''}".strip()
                user_id = user.id
                username = user.username

                # Get user join date
                join_date = datetime.utcfromtimestamp((await client.get_participants(event.chat_id, [user_id]))[0].joined_date).strftime('%Y-%m-%d %H:%M:%S')

                # Get total message count
                total_messages = 0
                async for message in client.iter_messages(entity=user_id, limit=None):
                    total_messages += 1

                # Get last message date
                async for message in client.iter_messages(entity=user_id, limit=1):
                    last_message_date = message.date.strftime('%Y-%m-%d %H:%M:%S')

                # Store user information in the database
                cursor.execute('''INSERT OR REPLACE INTO user_info 
                                  (user_id, username, full_name, join_date, total_messages, last_message_date) 
                                  VALUES (?, ?, ?, ?, ?, ?)''',
                               (user_id, username, user_full_name, join_date, total_messages, last_message_date))
                conn.commit()

                response_message = (
                    f"User ID: {user_id}\n"
                    f"Full Name: {user_full_name}\n"
                    f"Username: @{username if username else 'No username'}\n"
                    f"Join Date: {join_date}\n"
                    f"Total Messages: {total_messages}\n"
                    f"Last Message Date: {last_message_date}"
                )
                await event.respond(response_message)
                logger.info(f"Provided info for username {username}.")
            except Exception as e:
                await event.respond("Failed to retrieve information for the given username.")
                logger.error(f"Error retrieving user info: {str(e)}")
        else:
            await event.respond("Please provide a valid username after the /info command.")

    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())
