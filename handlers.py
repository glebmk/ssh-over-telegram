from key_gen import get_public_save_private_key

FILE_SECRET = 'private.key'


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='still under development')


def new_key(bot, update):
    public = get_public_save_private_key(file_secret=FILE_SECRET)
    bot.send_message(chat_id=update.message.chat_id, text=public.decode('utf-8'))


def bash(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text) # just echoing at this point
