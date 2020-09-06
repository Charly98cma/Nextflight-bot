#!/usr/bin/env python

# Telegram libraries
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# HTTP Requests
import requests

# Useful libraries
import datetime
import logging
import os
import sys

# Timezonefinder (coordinates --> TZ)
from timezonefinder import TimezoneFinder

# Useful for debuging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

# Basic URL of Launch Library API
URL = "https://ll.thespacedevs.com/2.0.0"

# Timezonefinder object
tf = TimezoneFinder()

# String with all the commands
commands_msg = "<b>Commands to control me:</b>\n" +\
        "/start - Start the conversation with me\n" +\
        "/help - Display the list of commands\n" +\
        "/next - Information about next lauch\n" +\
        "/cancel - Ends the conversation"

LOCATION, HELP, NEXT= range(3)

# List to save the TZ of the user (UTC by default)
userTZ = ['UTC']


def start_Command(update, context):
    logger.info('User {} starts a new conversation'.format(update.message.from_user.first_name))
    update.message.reply_text(
        text = "Hello there!\n\n" +\
        "I can help you keep track of the next rocket launch, you just need to ask :D\n\n" + commands_msg,
        parse_mode=ParseMode.HTML
    )
    update.message.reply_text(
        text = "But first, send me <b>your location</b> please, it's only used to give you the dates and times on your timezone.\n" +\
        "Use <b>/skip</b> if you dont want to give me your location.",
        parse_mode=ParseMode.HTML
    )
    return LOCATION


def location(update, context):
    location = update.message.location
    userTZ[0] = tf.timezone_at(
        lng = location["longitude"],
        lat = location["latitude"]
    )
    logger.info('User {} timezone is {}'.format(update.message.from_user.first_name, userTZ[0]))


def skip_location(update, context):
    logger.info('User {} didn\'t shared location'.format(update.message.from_user.first_name))
    update.message.reply_text(
        text = "Okey, dates and times will be <b>UTC</b> from now on.",
        parse_mode=ParseMode.HTML
    )


def help_Command(update, context):
    logger.info('User {} request the list of commands'.format(update.message.from_user.first_name))
    update.message.reply_text(
        commands_msg,
        parse_mode=ParseMode.HTML
    )


def nextflight_Command(update, context):
    logger.info('User {} request next space flight info'.format(update.message.from_user.first_name))
    # API request to retrieve the next space flight
    offset = 0
    # Loop to search the next launch because the API returns the most recent launch even if it has already happend
    while True:
        # mode can be "normal", "list", "detailed"
        results = requests.get(URL+"/launch/upcoming/", params={"limit" : 1, "offset" : offset, "mode" : "detailed"}).json()["results"][0]
        if (results["status"]["name"] not in ["Success", "Failed"]):
            break
        offset+=1

    # Name of rocket and payload
    name = results["name"]

    # Estimated launch date and time
    # REVIEW: Check the TZ works properly
    try:
        net = datetime.strptime(results["net"], "%Y-%m-%dT%H:%M:%SZ").astimezone(userTZ[0]).strftime("%Y %m %d - %H:%M:%S")
    except:
        net = "<i>Unknown launch date and time </i>"

    # Launch window start
    # REVIEW: Check the TZ works properly
    try:
        win_start = datetime.strptime(results["window_start"], "%Y-%m-%dT%H:%M:%SZ").astimezone(userTZ[0]).strftime("%Y %m %d - %H:%M:%S")
    except:
        win_start = "<i>Unknown window open date and time </i>"

    # Launch window end
    # REVIEW: Check the TZ works properly
    try:
        win_end = datetime.strptime(results["window_end"], "%Y-%m-%dT%H:%M:%SZ").astimezone(userTZ[0]).strftime("%Y %m %d - %H:%M:%S")
    except:
        win_end = "<i>Unknown window close date and time </i>"

    # Mission description
    try:
        mission_desc = results["mission"]["description"]
    except:
        mission_desc = "<i>Unknown description</i>"

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
        next_msg += "\n" + results["vidURLs"][0]["url"]
    except:
        pass
    
    # Infographic if there is one, otherwise, the image of the rocket
    try:
        update.message.reply_photo(
            results["infographic"],
            caption = next_msg,
            parse_mode = ParseMode.HTML
        )
    except:
        try:
            # Message with the available photo and the caption
            photo = results["image"]
            update.message.reply_photo(
                photo,
                caption = next_msg,
                parse_mode = ParseMode.HTML
            )
        except:
            # Message without photo since it is not available
            update.message.reply_text(
                text = next_msg,
                parse_mode=ParseMode.HTML
            )


def cancel_Command(update, context):
    update.message.reply_text(
        text = 'Bye! Has been a pleasure, hope we talk again soon!'
    )
    return ConversationHandler.END


def unknown_Command(update, context):
    logger.info('User {} send an unknown command {}'.format(update.message.from_user.first_name, update.message.text))
    update.message.reply_text(
        text = "Sorry, I didn't understand that command."
    )


def cancel_Command(update, context):
    logger.info('User {} ended conversation'.format(update.message.from_user.first_name))
    update.message.reply_text(
        "Bye! Hope we talk again soon :D"
    )
    return ConversationHandler.END


def cancel_Command(update, context):
    logger.info('User {} ended conversation'.format(update.message.from_user.first_name))
    update.message.reply_text("Bye! Hope we talk again soon")
    return ConversationHandler.END



def main():
    
    if 'NF_TOKEN' not in os.environ:
        print("Environment variable 'NF_TOKEN' not defined.", file=sys.stderr)
        exit(1)
    
    # FIXME: "use_context=True" should be removed once python-telegram-bot v13 is released on pip
    updater = Updater(os.environ.get('NF_TOKEN'), use_context=True)

    # Dispatcher to register handlers
    dp = updater.dispatcher

    # Handlers
    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start', start_Command)],
        
        states = {
            LOCATION : [MessageHandler(Filters.location, location)]
        },
        
        fallbacks = [CommandHandler('skip', skip_location)]
    )

    dp.add_handler(conv_handler)

    dp.add_handler(CommandHandler('help', help_Command))
    dp.add_handler(CommandHandler('nextflight', nextflight_Command))
    dp.add_handler(CommandHandler('cancel', cancel_Command))
    dp.add_handler(MessageHandler(Filters.command, unknown_Command))
    
    
    # Starts the bot
    updater.start_polling(clean = True)
    updater.idle()

if __name__ == '__main__':
    main()
