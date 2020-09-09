# Package to send messages with HTML format
from telegram import ParseMode

def send_txtMsg(update, message):
    update.message.reply_text(
        text = message,
        parse_mode = ParseMode.HTML
    )

def send_photoMsg(update, message, photo):
    update.message.reply_photo(
        photo,
        caption = message,
        parse_mode = ParseMode.HTML
    )
