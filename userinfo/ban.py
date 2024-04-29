from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatPermissions
import logging
import config

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the function to handle the /ban command
def ban(update, context):
    user_id = update.message.reply_to_message.from_user.id
    context.bot.restrict_chat_member(update.effective_chat.id, user_id, ChatPermissions(), until_date=None)
    update.message.reply_text(f"User {update.message.reply_to_message.from_user.name} has been banned from the group.")

# Define the function to handle the /unban command
def unban(update, context):
    user_id = update.message.reply_to_message.from_user.id
    context.bot.restrict_chat_member(update.effective_chat.id, user_id, ChatPermissions(restrict_everyone=False))
    update.message.reply_text(f"User {update.message.reply_to_message.from_user.name} has been unbanned from the group.")

# Define the function to handle regular messages
def echo(update, context):
    update.message.reply_text("I'm sorry, I don't understand that command.")

# Set up the bot and its handlers
def main():
    updater = Updater(config.TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("ban", ban))
    dp.add_handler(CommandHandler("unban", unban))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
