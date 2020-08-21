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

# String with all the commands
commands_msg = "<b>Commands to control me:</b>\n" +\
        "/start - Start the conversation with me\n" +\
        "/help - Display the list of commands\n" +\
        "/next - Information about next lauch\n" +\
        "/cancel - Ends the conversation"


# Processing commands
def start_Command(update, context):
    welcome_msg = "Hello there!\n\n" +\
        "I can help you keep track of the next rocket launch, you just need to ask :D\n\n" + commands_msg
        
    update.message.reply_text(welcome_msg, parse_mode=ParseMode.HTML)

    # TODO: Ask timezone for dates (if user rejects, use UTC)

    
def help_Command(update, context):
    # Gives the user the list of commands
    update.message.reply_text(commands_msg, parse_mode=ParseMode.HTML)

    
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

    # Estimated launch date and time
    try:
        net = datetime.strptime(results["net"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y %m %d - %H:%M:%S UTC")
    except:
        net = "<i>Unknown launch date and time </i>"
        
    # Launch window start
    try:
        win_start = datetime.strptime(results["window_start"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y %m %d - %H:%M:%S UTC")
    except:
        win_start = "<i>Unknown wind. open date and time </i>"

    # Launch window end
    try:    
        win_end = datetime.strptime(results["window_end"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y %m %d - %H:%M:%S UTC")
    except:
        win_start = "<i>Unknown wind. close date and time </i>"

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

        
    # Message for the user
    next_msg = "<b>" + name + "</b>\n\n" +\
        "NET: " + net + "\n" +\
        "Wind.Open: " + win_start + "\n" +\
        "Wind.Close: " + win_end + "\n\n" +\
        mission_desc + "\n\n" +\
        mission_orbit + " - " + mission_type + "\n" +\
        pad + " - " + location

    # URL of the streaming
    try:
        vidURL = results["vidURLs"][0]["url"]
        next_msg += "\n" + vidURL
    except:
        pass

    update.message.reply_text(next_msg, parse_mode=ParseMode.HTML)

    
    # TODO: Ask if user wants infographic (see how to implement it)
    # update.message.reply_photo(...)
        

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




