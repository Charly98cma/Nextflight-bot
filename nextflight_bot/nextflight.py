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
userTZ = [pytz.utc]
# Timezonefinder object
tf = TimezoneFinder()


def start_Command(update, context):
    """Start command explaining what can do this bot and asking for user location."""
    logger.info('User {} starts a new conversation'.format(update.message.from_user.first_name))
    msgMng.send_txtMsg(update, msgs.welcome_msg)
    msgMng.send_txtMsg(update, msgs.location_msg)
    return LOCATION


def location(update, context):
    """User shared location, and is used to 'calculate' its TZ."""
    tz = tf.timezone_at(
        lng = update.message.location["longitude"],
        lat = update.message.location["latitude"]
    )
    msgMng.send_txtMsg(update, msgs.timezone_msg + tz)
    logger.info('User {} timezone is {}'.format(update.message.from_user.first_name, tz))
    userTZ[0] = pytz.timezone(tz)
    return LOOP


def skip_location(update, context):
    """User doesn't want to share location, so UTC will be used."""
    logger.info('User {} didn\'t shared location'.format(update.message.from_user.first_name))
    msgMng.send_txtMsg(update, msgs.skip_location_msg)
    return LOOP


def help_Command(update, context):
    """User asked for the list of commands."""
    logger.info('User {} request the list of commands'.format(update.message.from_user.first_name))
    msgMng.send_txtMsg(update, msgs.commands_msg)
    return LOOP


def nextflight_Command(update, context):
    """User asked for information about the space flight."""
    logger.info('User {} request next space flight info'.format(update.message.from_user.first_name))
    next_msg, photo = next_Command(userTZ)
    """Based on the photo/infographic availability, the text does or doesn't include the photo"""
    if photo is not None:
        msgMng.send_photoMsg(update, next_msg, photo)
    else:
        msgMng.send_txtMsg(update, next_msg)
    return LOOP


def unknown_Command(update, context):
    """User introduced an unknown command."""
    logger.info('User {} send an unknown command {}'.format(update.message.from_user.first_name, update.message.text))
    msgMng.send_txtMsg(update, msgs.unknown_msg)
    return LOOP


def cancel_Command(update, context):
    logger.info('User {} ended conversation'.format(update.message.from_user.first_name))
    msgMng.send_txtMsg(update, msgs.cancel_msg)
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    if 'NF_TOKEN' not in os.environ:
        print("Environment variable 'NF_TOKEN' not defined.", file=sys.stderr)
        exit(1)

    # FIXME: "use_context=True" should be removed once python-telegram-bot v13 is released on pip
    updater = Updater(
        token = os.environ.get('NF_TOKEN'),
        use_context = True)

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
                CommandHandler('cancel', cancel_Command),
                MessageHandler(Filters.command, unknown_Command)
            ]
        },

        fallbacks = [
            CommandHandler('cancel', cancel_Command)
        ],
        # Let the user restart the conversation at any point
        allow_reentry = True
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)

    # Starts the bot
    updater.start_polling(
        clean = False)
    updater.idle()

if __name__ == '__main__':
    main()
