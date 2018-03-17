import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, DispatcherHandlerStop
from handlers import new_key, start, bash

token_path = '/Users/gleb/secret/tg_bot1_token'
username = 'glebmakarchuk'

with open(token_path, 'r') as f:
    token = f.read().strip()

bot = telegram.Bot(token=token)
print(bot.get_me())

updater = Updater(token=token)
dispatcher = updater.dispatcher


def check_user(_, update):
    if update.message.from_user.username != username:
        raise DispatcherHandlerStop


dispatcher.add_handler(MessageHandler(Filters.all, check_user), group=-1)

dispatcher.add_handler(CommandHandler('start', start))

dispatcher.add_handler(CommandHandler('newkey', new_key))

dispatcher.add_handler(MessageHandler(Filters.text, bash))

updater.start_polling()
