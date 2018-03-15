import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from handlers import new_key, start, bash

token_path = '/Users/gleb/secret/tg_bot1_token'

with open(token_path, 'r') as f:
    token = f.read().strip()

bot = telegram.Bot(token=token)
print(bot.get_me())

updater = Updater(token=token)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

new_key_handler = CommandHandler('newkey', new_key)
dispatcher.add_handler(new_key_handler)

bash_handler = MessageHandler(Filters.text, bash)
dispatcher.add_handler(bash_handler)

updater.start_polling()
