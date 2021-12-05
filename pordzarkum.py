import logging
import telegram
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update,ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
tek=0
state_name = ["Տեքստ","Լուսավորություն","Դերասաններ","Վայր"]
state = ["","","",""]
derasanner = ['Հայկո',"Մկո","Անդո","Երեխա"]
vayrer = ["տուն","հիվանդանոց","դուրս","ննջասենյակ","բանտ","գժանոց"]
updater = Updater("2115330440:AAHufJG8fmYXzukBmEtaF102WioPkcVgJFs", use_context=True)
j =updater.job_queue
def start(update, context):
    global state
    bot = telegram.Bot(token="2115330440:AAHufJG8fmYXzukBmEtaF102WioPkcVgJFs")
    #bot.send_message(813402616,update.message.chat_id)
    state = ["","","",""]
    user = update.message.from_user
    update.message.reply_text("Սկսենք",reply_markup=main_menu())

def print_state(query,func,edit=True):
  text = ""
  for i in range(4):
    text+=f"{state_name[i]} -- {state[i]}\n"
  if edit:
    query.edit_message_text(text,reply_markup=func())
  else:
    query.message.reply_text(text,reply_markup=func())
def main_menu():
    keyboard = [[
          InlineKeyboardButton("Պատահական 🎲", callback_data='1'),
          InlineKeyboardButton("Փնտրել 🔎", callback_data='2')],[InlineKeyboardButton("Հետաքրքիր փաստեր", callback_data='3')]]
    return InlineKeyboardMarkup(keyboard)
def choose():
    keyboard = [[
          InlineKeyboardButton("Տեքստ 📃", callback_data='te'),
          InlineKeyboardButton("Դերասաններ 👫🏻", callback_data='de')],
          [InlineKeyboardButton("Լուսավորություն 💡", callback_data='svet'),
          InlineKeyboardButton("Վայր 🏡", callback_data='vayr')],
          [InlineKeyboardButton("Փնտրել 🔎", callback_data='search')]]
    
    return InlineKeyboardMarkup(keyboard)
def inter():
  keyboard = [[
          InlineKeyboardButton("Ամենաերկար", callback_data='erkar'),
          InlineKeyboardButton("Ամենակարճ", callback_data='karch')],
          [InlineKeyboardButton("Ամենահին", callback_data='hin'),
          InlineKeyboardButton("Ամենանոր", callback_data='nor')],
          [InlineKeyboardButton("Ամենահավանված", callback_data='havanel'),
          InlineKeyboardButton("Ամենամեկնաբանված", callback_data='comment')]]
    
  return InlineKeyboardMarkup(keyboard)

def vayr():
  keyboard = [[InlineKeyboardButton(i, callback_data=f'vayr-{i}'),
          InlineKeyboardButton(j, callback_data=f'vayr-{j}')] for i,j in zip(vayrer[::2],vayrer[1::2])]
  return InlineKeyboardMarkup(keyboard)

def derasan():
  keyboard = [[InlineKeyboardButton(i, callback_data=f'der-{i}'),
          InlineKeyboardButton(j, callback_data=f'der-{j}')] for i,j in zip(derasanner[::2],derasanner[1::2])]
  keyboard.append([InlineKeyboardButton("վերջ", callback_data='back')])
  return InlineKeyboardMarkup(keyboard)
def luys():
  keyboard = [[
          InlineKeyboardButton("լուսավոր", callback_data='lԼուսավոր'),
          InlineKeyboardButton("մութ", callback_data='lմութ')],
          [InlineKeyboardButton("մութ -> լուսավոր", callback_data='lմութ -> լուսավոր'),
          InlineKeyboardButton("լուսավոր -> մութ", callback_data='lլուսավոր -> մութ')]]
    
  return InlineKeyboardMarkup(keyboard)
def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def echo(update, context):
    global tek
    if tek==1:
      text=update.message.text
      #r = requests.post(url="http://192.168.8.156:509/api", 
      #json={'text': update.message.text, 'filters':{'Վայր':'Տուն'}})
      #update.message.reply_text(r.json()['url'])
      state[0]=text
      print_state(update,choose ,False)
      tek=0
    if update.message.text == "դու փիղ ես":
        update.message.reply_text("Այո բայց ոչ սովորական , այլ ԿԱՐԳԻՆ ՓԻՂ🐘")
    #else:
        #update.message.reply_text("https://www.youtube.com/watch?v=pi2au8rx0XQ&list=PLDDuEZQEC_uAuSrUXsFVBLNkPQY3BHzLQ&index=6")
        #update.message.reply_text("https://www.youtube.com/watch?v=cfOEjPZk6FA")

def button(update, context):
    """Parses the CallbackQuery and updates the message text."""
    global lusaworutyun,state
    query = update.callback_query
    query.answer()
    if query.data=='1':
      #r=requests.get('http://192.168.8.156:509/')
      #query.edit_message_text(r.json()['url'])
      query.message.reply_text("Ընտրեք",reply_markup=main_menu())
    elif query.data=='2':
      query.edit_message_text("Ի՞նչ եք հիշում",reply_markup=choose())
    elif query.data=='te':
      global tek
      query.edit_message_text("Գրեք ձեր հիշած հատվածը")
      tek=1
    elif query.data=='svet':
      print_state(query,luys)
    elif query.data=='3':
      print_state(query,inter)
    elif query.data[0]=='l':
      state[1] = query.data[1:]
      print_state(query,choose)
    elif query.data=="vayr":
      print_state(query,vayr)
    elif query.data=="de":
      print_state(query,derasan)
    elif query.data=="back":
      print_state(query,choose)
    elif "vayr" in query.data:
      state[3] = query.data[5:]
      print_state(query,choose)
    elif "der" in query.data:
      if not (query.data[4:] in state[2]):
        state[2]+=query.data[4:]+"  "
      print_state(query,derasan)
    elif query.data=='search':
      state = ["","","",""]
      query.edit_message_text("ֆունկցիան դեռ չի աշխատում",reply_markup=main_menu())
      #j.run_once(query.edit_message_text("Տղեք , կատակ էի անում , հետ էկեք "),100)

def error(update,context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():

    #bot = telegram.Bot(token="2115330440:AAHufJG8fmYXzukBmEtaF102WioPkcVgJFs")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
