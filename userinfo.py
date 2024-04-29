
from telethon import TelegramClient, events

# Replace these with your own API ID and hash
api_id = '27913018'
api_hash = '04e2f4e414cdabe52ad985adaa6cfe09'

# Replace this with your bot token
bot_token = '7091541433:AAHHwt431VqrI3jkYPaEMDmCxZ9PFTvs5f8'

# Create a Telegram client object
client = TelegramClient('my_bot', api_id, api_hash).start(bot_token=bot_token)

# Define a handler function for the /info command
async def handle_info_command(event):
    user = await event.get_sender()
    first_name = user.first_name
    last_name = user.last_name
    username = user.username
    mention = f'[{first_name} {last_name}]({username})'
    text = f'Hi {mention}! Here is your information:\n\nFirst name: {first_name}\nLast name: {last_name}\nUsername: {username}'
    await event.respond(text)

# Register the handler function for the /info command
client.add_event_handler(handle_info_command, events.NewMessage(pattern='/info'))

# Run the bot until it's stopped manually
client.run_until_disconnected()
