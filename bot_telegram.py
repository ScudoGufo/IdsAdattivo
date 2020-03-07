from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackContext
from telegram.ext import MessageHandler, Filters
import bot_info_wrapper
import bot_database
import bot_main

TELEGRAM_API_KEY=""
MY_CHAT_ID=""

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def send_request_event(context: CallbackContext):
    msg = context.job.context
    context.bot.send_message(chat_id=MY_CHAT_ID, text=msg)

def send_alert(client, intelipapi, intelshodan, job):
	msg = bot_info_wrapper.get_info(client, intelipapi, intelshodan)
	job.run_once(send_request_event,1, context=msg)

def info_db(update, context):
	global cursor
	msg = bot_database.get_info(cursor)
	context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def close(updater):
    updater.stop()
    updater.is_idle = False
    print('[*] Telegram Pollig Stopped')

def init(cursor_tmp):

	global cursor
	cursor = cursor_tmp

	updater = Updater(token=TELEGRAM_API_KEY, use_context=True)
	dispatcher = updater.dispatcher
	job = updater.job_queue
	updater.start_polling()


	dbInfoHandler = CommandHandler('infodb', info_db)
	dispatcher.add_handler(dbInfoHandler)

	print('[*] Telegram Pollig Started')
	return [updater, job]

#echo_handler = MessageHandler(Filters.text, echo)
#start_handler = CommandHandler('start', start)
#dispatcher.add_handler(echo_handler)
#dispatcher.add_handler(start_handler)

