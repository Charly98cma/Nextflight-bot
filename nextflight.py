# TELEGRAM LIBRARIES
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler

# LAUNCHLIBRARY
import launchlibrary as ll 

# USEFUL LIBRARIES
import logging
from datetime import datetime

# ENVIROMENT VARIABLES
import os


# Processing commands
def startCommand(bot, update):
    welcome_message = "Hola :D"
    context.bot.send_message(chat_id = update.message.chat.id, text = welcome_message, parse_mode = ParseMode.MARKDOWN)


def helpCommand(bot, update):
    h = "WIP"

def nextflightCommand(bot, update):
    h = "WIP"

# Connection with the bot
# FIXME: use_context should be removed once python-telegram-bot 
updater = Updater(os.environ.get('NF_TOKEN'), use_context=True)
dp = updater.dispatcher

# Useful configuration for debuging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Initializing API connection (retries is optional)
api = ll.Api()

# Handlers for commands
dp.add_handler(CommandHandler('start', startCommand))
dp.add_handler(CommandHandler('help', helpCommand))
dp.add_handler(CommandHandler('nextflight', nextflightCommand))

# Getting starter for Updates
updater.start_polling(clean = True)


# Stop the bot if Ctrl+C is pressed
updater.idle()






