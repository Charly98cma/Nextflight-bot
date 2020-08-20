# TELEGRAM LIBRARIES
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, MessageHandler

# HTTP Requests
import requests

# USEFUL LIBRARIES
import logging
from datetime import datetime

# ENVIROMENT VARIABLES
import os


# Useful for debuging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Basic URL of Launch Library API
URL = "https://ll.thespacedevs.com/2.0.0"


# Processing commands
def start_Command(update, context):
    welcome_msg = "Hello there!\n\n" +\
        "I can help you keep track of the next rocket launch, you just need to ask :D\n\n" +\
        "<b>Commands to control me:</b>\n" +\
        "/start - Start the conversation with me\n" +\
        "/help - Display the list of commands\n" +\
        "/next - Information about next lauch(some info might be classified)\n" +\
        "/cancel - Ends the conversation"
    update.message.reply_text(welcome_msg, parse_mode=ParseMode.HTML)

    
def help_Command(update, context):
    # Gives the user the list of commands
    help_msg = "<b>Commands to control me:</b>\n" +\
        "/start - Start the conversation with me\n" +\
        "/help - Display the list of commands\n" +\
        "/next - Information about next lauch (some info might be classified)\n" +\
        "/cancel - Ends the conversation"
    update.message.reply_text(help_msg, parse_mode=ParseMode.HTML)

    
def nextflight_Command(update, context):
    # API request to retrieve the next space flight
    offset = 0
    # Loop to search the next launch because the API returns the most recent launch even if it has already happend
    while True:
        # mode can be "normal", "list", "detailed"
        response = requests.get(URL+"/launch/upcoming/", params={"limit" : 1, "offset" : offset, "mode" : "detailed"}).json()
        results = response["results"][0]
        if (results["status"]["name"] not in ["Success", "Failed"]):
            break
        offset+=1

    # Name of rocker and payload
    name = results["name"]

    # TODO: Check if net, win_start, win_end could be null (Chinese gov give very little info)

    # Estimated launch date and time
    net = datetime.strptime(results["net"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y %m %d - %H:%M:%S UTC")

    # Launch window start
    win_start = datetime.strptime(results["window_start"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y %m %d - %H:%M:%S UTC")

    # Launch window end
    win_end = datetime.strptime(results["window_end"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y %m %d - %H:%M:%S UTC")

    # Mission description
    try:
        mission_desc = results["mission"]["description"]
    except:
        mission_desc = "<i>No description given</i>"

    # Abbreviation of mission orbit
    try:
        mission_orbit = results["mission"]["orbit"]["abbrev"]
    except:
        mission_orbit = "<i>Unknown orbit</i>"

    # Mission type
    try:
        mission_type = results["mission"]["type"]
    except:
        mission_type = "<i>Unknown mission type</i>"

    # Launch location
    try:
        location = results["pad"]["location"]["name"]
    except:
        location = "<i>Unknown location</i>"

    # Launch pad
    try:
        pad = results["pad"]["name"]
    except:
        pad = "<i>Unknown launch pad</i>"


    # TODO: Add URLs to streams, if there is no stream photo of rocket

    # TODO: Ask if user wants infographic (see how to implement it)
        
    # Full message to the user
    next_msg = "<b>" + name + "</b>\n\n" +\
        "<i>NET</i>: " + net + "\n" +\
        "<i>Win.Start</i>: " + win_start + "\n" +\
        "<i>Win.Close</i>: " + win_end + "\n\n" +\
        mission_desc + "\n\n" +\
        mission_orbit + " - " + mission_type + "\n" +\
        pad + " - " + location
    update.message.reply_text(next_msg, parse_mode=ParseMode.HTML)


def unknown_Command(update, context):
    update.message.reply_text("Sorry, I didn't understand that command.")



    
def main():
    # Connection with the bot (the first argument is your token)
    # FIXME: use_context should be removed once python-telegram-bot v13 is released on pip
    updater = Updater(os.environ.get('NF_TOKEN'), use_context=True)
    
    # Dispatcher to register handlers
    dp = updater.dispatcher
    
    # Handlers for commands
    dp.add_handler(CommandHandler('start', start_Command))
    dp.add_handler(CommandHandler('help', help_Command))
    dp.add_handler(CommandHandler('nextflight', nextflight_Command))
    dp.add_handler(MessageHandler(Filters.command, unknown_Command))
    
    # Getting starter for Updates
    updater.start_polling(clean = True)
    updater.idle()


if __name__ == '__main__':
    main()




