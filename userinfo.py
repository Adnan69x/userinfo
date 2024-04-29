import logging
from telethon import TelegramClient, events
import config

# Set up logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# Telethon client setup
client = TelegramClient('bot', config.API_ID, config.API_HASH).start(bot_token=config.BOT_TOKEN)

async def print_user_information(event):
    # Getting user info
    if event.is_private:  # Checks if the event is a private message
        user = await event.get_sender()
        user_full_name = user.first_name
        if user.last_name:
            user_full_name += ' ' + user.last_name
        
        last_update = user.status
        if last_update:
            last_update = f'{last_update.__class__.__name__} at {last_update.was_online if hasattr(last_update, "was_online") else "N/A"}'
        else:
            last_update = 'N/A'
        
        print(f'User ID: {user.id}')
        print(f'Full Name: {user_full_name}')
        print(f'Username: {user.username if user.username else "No username"}')
        print(f'Last update: {last_update}')

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    # Reply with user information when the bot receives /start command
    await print_user_information(event)
    await event.respond('Here is your information!')

def main():
    with client:
        client.run_until_disconnected()

if __name__ == '__main__':
    main()
