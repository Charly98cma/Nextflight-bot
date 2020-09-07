#!/usr/bin/env python

# Telegram libraries
from telegram import Update, ParseMode
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

# Useful for debuging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

# Timezonefinder object
tf = TimezoneFinder()

LOCATION = range(1)

# List to save the TZ of the user (UTC by default)
userTZ = ['UTC', pytz.utc]

def start_Command(update, context):
    logger.info('User {} starts a new conversation'.format(update.message.from_user.first_name))
    update.message.reply_text(
        text = msgs.welcome_msg,
        parse_mode = ParseMode.HTML
    )
    update.message.reply_text(
        text = msgs.location_msg,
        parse_mode = ParseMode.HTML
    )
    return LOCATION


def location(update, context):
    location = update.message.location
    userTZ[0] = tf.timezone_at(
        lng = location["longitude"],
        lat = location["latitude"]
    )
    userTZ[1] = pytz.timezone(
        userTZ[0]
    )
    locFlag = True
    update.message.reply_text(
        text = msgs.timezone_msg + userTZ[0],
        parse_mode = ParseMode.HTML
    )
    logger.info('User {} timezone is {}'.format(update.message.from_user.first_name, userTZ[0]))


def skip_location(update, context):
    if locFlag:
        pass
    logger.info('User {} didn\'t shared location'.format(update.message.from_user.first_name))
    update.message.reply_text(
        text = msgs.skip_location_msg,
        parse_mode = ParseMode.HTML
    )
    locFlag = True


def help_Command(update, context):
    logger.info('User {} request the list of commands'.format(update.message.from_user.first_name))
    update.message.reply_text(
        msgs.commands_msg,
        parse_mode = ParseMode.HTML
    )


def nextflight_Command(update, context):
    logger.info('User {} request next space flight info'.format(update.message.from_user.first_name))

    next_msg, photo = next_Command(userTZ)
    
    if photo is not None:
        # Message with photo or infographic
        update.message.reply_photo(
            photo,
            caption = next_msg,
            parse_mode = ParseMode.HTML
        )
    else:
        # Message without photo since it is not available
        update.message.reply_text(
            text = next_msg,
            parse_mode = ParseMode.HTML
        )


def unknown_Command(update, context):
    logger.info('User {} send an unknown command {}'.format(update.message.from_user.first_name, update.message.text))
    update.message.reply_text(
        text = msgs.unknown_msg
    )


def cancel_Command(update, context):
    logger.info('User {} ended conversation'.format(update.message.from_user.first_name))
    update.message.reply_text(
        text = msgs.cancel_msg
    )
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

    # Flag for location already set 
    locFlag = False

    
    # Starts the bot
    updater.start_polling(clean = True)
    updater.idle()

if __name__ == '__main__':
    main()
