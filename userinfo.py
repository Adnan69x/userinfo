import logging
from telethon import TelegramClient, events
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError, TelethonError
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantsAdmins
import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Telegram Client
client = TelegramClient('bot_session', config.API_ID, config.API_HASH)

async def main():
    await client.start(bot_token=config.BOT_TOKEN)
    logger.info("Bot has been started successfully.")

    @client.on(events.NewMessage(pattern=r'/info(?: (\@\w+))?'))
    async def handler(event):
        username = event.pattern_match.group(1)  # Extract the username from the command

        if event.is_group:
            try:
                entity = await client.get_entity(event.chat)
                if username:  # If a username is provided in the command
                    try:
                        participant_info = await client(GetParticipantRequest(
                            channel=entity,
                            participant=username
                        ))
                        participant = participant_info.participant
                        user = await client.get_entity(username)
                    except UserNotParticipantError:
                        await event.respond(f"The user {username} is not a member of this group or has privacy settings blocking this.")
                        return
                else:
                    user = await event.get_sender()  # If no username, get info of the sender
                    participant = await client(GetParticipantRequest(
                        channel=entity,
                        participant=user.id
                    )).participant

                situation = 'Admin' if isinstance(participant, ChannelParticipantAdmin) else 'Member'
                roles = participant.rank if hasattr(participant, 'rank') and participant.rank else 'No specific role'
                join_date = participant.date if hasattr(participant, 'date') else 'Unknown'
                
                info = (
                    f"ID: {user.id}\n"
                    f"Name: {user.first_name} {user.last_name if user.last_name else ''}\n"
                    f"Username: @{user.username if user.username else 'No username'}\n"
                    f"Situation: {situation}\n"
                    f"Roles: {roles}\n"
                    f"Join: {join_date}\n"
                    f"Messages: 'Not available due to API limitations'\n"
                    f"Last Message: 'Not available due to API limitations'"
                )
                await event.respond(info)
            except TelethonError as e:
                await event.respond("Failed to retrieve information for the given username due to a Telegram API error.")
                logger.error(f"Telethon API Error: {str(e)}")
        else:  # Handling the command in private chats
            user = await event.get_sender()
            last_update = user.status
            last_update_desc = f'{last_update.__class__.__name__} at {last_update.was_online if hasattr(last_update, "was_online") else "N/A"}' if last_update else 'N/A'

            personal_info = (
                f"User ID: {user.id}\n"
                f"Full Name: {user.first_name} {user.last_name if user.last_name else ''}\n"
                f"Username: @{user.username if user.username else 'No username'}\n"
                f"Last update: {last_update_desc}"
            )
            await event.respond(personal_info)
            logger.info(f"Provided personal info for user {user.id}.")

    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())
