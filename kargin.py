import logging
import telegram
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
tek=0
def start(update, context):
    update.message.reply_text("Բարև կարգին նայող կարգին տղա",reply_markup=main_menu())

def main_menu():
    keyboard = [[
          InlineKeyboardButton("random", callback_data='1'),
          InlineKeyboardButton("search", callback_data='2'),],]
    return InlineKeyboardMarkup(keyboard)
def choose():
    keyboard = [[
          InlineKeyboardButton("text", callback_data='te'),
          InlineKeyboardButton("derasanner", callback_data='de'),
          InlineKeyboardButton("lusavorutyun", callback_data='lu'),
          InlineKeyboardButton("vayr", callback_data='va'),],]
    return InlineKeyboardMarkup(keyboard)
def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def echo(update, context):
    global tek
    if tek==1:
      update.message.reply_text("da")
      r=requests.get('http://192.168.8.156:509/')
      update.message.reply_text(r.json()['url'])
      update.message.reply_text("da")
      tek=0
    if update.message.text == "դու փիղ ես":
        update.message.reply_text("Այո բայց ոչ սովորական , այլ ԿԱՐԳԻՆ ՓԻՂ🐘")
    #else:
        #update.message.reply_text("https://www.youtube.com/watch?v=pi2au8rx0XQ&list=PLDDuEZQEC_uAuSrUXsFVBLNkPQY3BHzLQ&index=6")
        #update.message.reply_text("https://www.youtube.com/watch?v=cfOEjPZk6FA")

def button(update, context):
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    query.answer()
    if query.data=='1':
      #update.message.reply_text("https://www.youtube.com/watch?v=pi2au8rx0XQ&list=PLDDuEZQEC_uAuSrUXsFVBLNkPQY3BHzLQ&index=6")
      query.edit_message_text("https://www.youtube.com/watch?v=pi2au8rx0XQ&list=PLDDuEZQEC_uAuSrUXsFVBLNkPQY3BHzLQ&index=6")

      query.message.reply_text("ntreq",reply_markup=main_menu())
    elif query.data=='2':
      query.edit_message_text("incheq hishum",reply_markup=choose())
    elif query.data=='te':
      global tek
      query.edit_message_text("incheq hishum")
      tek=1

def error(update,context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    updater = Updater("2115330440:AAHufJG8fmYXzukBmEtaF102WioPkcVgJFs", use_context=True)
    #bot = telegram.Bot(token="2115330440:AAHufJG8fmYXzukBmEtaF102WioPkcVgJFs")
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler("help", help))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
    # log all errors
    dp.add_error_handler(error)
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
