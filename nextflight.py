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


# Useful for debuging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


# Processing commands
def start_Command(update, context):
    welcome_message = 'Hello there :D\n' + \
        'I can help you keep track of the next rocket launch.\n\n' + \
        '**Commands to control me:c**\n' +\
        '*/help* - Display the list of commands\n' +\
        '*/next* - Information about next lauch\n' +\
        '*/cancel* - Ends the conversation'
    update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN)

    
def help_Command(update, context):
    h = "WIP"

    
def nextflight_Command(update, context):
    h = "WIP"


def cancel_Command(update, context):
    h = "WIP"



    
def main():
    # Connection with the bot
    # FIXME: use_context should be removed once python-telegram-bot v13 is released on pip
    updater = Updater(os.environ.get('NF_TOKEN'), use_context=True)
    
    # Dispatcher to register handlers
    dp = updater.dispatcher
    
    # Initializing Launchlibrary API connection
    api = ll.Api()
    
    # Handlers for commands
    dp.add_handler(CommandHandler('start', start_Command))
    dp.add_handler(CommandHandler('help', help_Command))
    dp.add_handler(CommandHandler('nextflight', nextflight_Command))
    dp.add_handler(CommandHandler('cancel', cancel_Command))
    
    # Getting starter for Updates
    updater.start_polling(clean = True)
    updater.idle()


if __name__ == '__main__':
    main()




