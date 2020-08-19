# TELEGRAM LIBRARIES
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler

# LAUNCHLIBRARY
import requests

# USEFUL LIBRARIES
import logging
from datetime import datetime

# ENVIROMENT VARIABLES
import os


# Useful for debuging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Basic URL of the API
URL = "https://ll.thespacedevs.com/2.0.0"


# Processing commands
def start_Command(update, context):
    welcome_msg = "Hello there!\n" + \
        "I can help you keep track of the next rocket launch, you just need to ask :D\n\n" + \
        "<b>Commands to control me:</b>\n" +\
        "/help - Display the list of commands\n" +\
        "/next - Information about next lauch\n" +\
        "/cancel - Ends the conversation"
    update.message.reply_text(welcome_msg, parse_mode=ParseMode.HTML)

    
def help_Command(update, context):
    # Gives the user the list of commands
    help_msg = "<b>Commands to control me:</b>\n" +\
        "/help - Display the list of commands\n" +\
        "/next - Information about next lauch\n" +\
        "/cancel - Ends the conversation"
    update.message.reply_text(help_msg, parse_mode=ParseMode.HTML)

    
def nextflight_Command(update, context):
    # API request to retrive the next space flight
    response = requests.get(URL+"/launch", params={"limit" : 1}).json()
    results = response["results"][0]
    name = results["name"]
    
    #update.message.reply_text(results["name"], parse_mode=ParseMode.HTML)


def cancel_Command(update, context):
    h = "WIP"


    
def main():
    # Connection with the bot
    # FIXME: use_context should be removed once python-telegram-bot v13 is released on pip
    updater = Updater(os.environ.get('NF_TOKEN'), use_context=True)
    
    # Dispatcher to register handlers
    dp = updater.dispatcher
    
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




