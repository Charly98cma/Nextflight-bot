#!/usr/bin/env python

# Telegram libraries
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
# Useful libraries
import logging
import os
import sys
# Package to manage timezones
import pytz
# Timezonefinder (coordinates --> TZ)
from timezonefinder import TimezoneFinder
# Messages and texts send to the user
import messages as msgs
# Code of /nextflight
from flight_info import next_Command
# Code for sending the message to the user
import msg_management as msgMng


# Useful for debuging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

LOCATION, LOOP = range(2)

# List to save the TZ of the user (UTC by default)
userTZ = ['UTC', pytz.utc]
# Flag for location already set 
locFlag = False
# Timezonefinder object
tf = TimezoneFinder()


def start_Command(update, context):
    logger.info('User {} starts a new conversation'.format(update.message.from_user.first_name))
    msgMng.send_txtMsg(update, msgs.welcome_msg)
    msgMng.send_txtMsg(update, msgs.location_msg)
    return LOCATION


def location(update, context):
    global locFlag
    locFlag = True    
    location = update.message.location
    userTZ[0] = tf.timezone_at(
        lng = location["longitude"],
        lat = location["latitude"]
    )
    userTZ[1] = pytz.timezone(
        userTZ[0]
    )
    msgMng.send_txtMsg(update, msgs.timezone_msg + userTZ[0])
    logger.info('User {} timezone is {}'.format(update.message.from_user.first_name, userTZ[0]))
    return LOOP


def skip_location(update, context):
    global locFlag
    if locFlag:
        pass
    logger.info('User {} didn\'t shared location'.format(update.message.from_user.first_name))
    msgMng.send_txtMsg(update, msgs.skip_location_msg)
    locFlag = True
    return LOOP


def help_Command(update, context):
    logger.info('User {} request the list of commands'.format(update.message.from_user.first_name))
    msgMng.send_txtMsg(update, msgs.commands_msg)
    return LOOP


def nextflight_Command(update, context):
    logger.info('User {} request next space flight info'.format(update.message.from_user.first_name))
    next_msg, photo = next_Command(userTZ)
    if photo is not None:
        # Message with photo or infographic
        msgMng.send_photoMsg(update, next_msg, photo)
    else:
        # Message without photo since it is not available
        msgMng.send_txtMsg(update, next_msg)
    return LOOP


def unknown_Command(update, context):
    logger.info('User {} send an unknown command {}'.format(update.message.from_user.first_name, update.message.text))
    msgMng.send_txtMsg(update, msgs.unknown_msg)
    return LOOP


def cancel_Command(update, context):
    logger.info('User {} ended conversation'.format(update.message.from_user.first_name))
    msgMng.send_txtMsg(update, msgs.cancel_msg)
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
            LOCATION : [
                MessageHandler(Filters.location, location),
                CommandHandler('skip', skip_location)
            ],
            LOOP : [
                CommandHandler('help', help_Command),
                CommandHandler('nextflight', nextflight_Command),
                MessageHandler(Filters.command, unknown_Command)
            ]
        },
        
        fallbacks = [
            CommandHandler('cancel', cancel_Command)
        ]
    )

    dp.add_handler(conv_handler)

    # Starts the bot
    updater.start_polling(clean = True)
    updater.idle()

if __name__ == '__main__':
    main()
