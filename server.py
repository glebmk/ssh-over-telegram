import argparse
import configparser
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, DispatcherHandlerStop
from handlers import new_key, start, bash
from functools import partial


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('config_path',
                        help='Path to the bot config',
                        default='config',
                        nargs='?',
                        type=str)

    config_path = parser.parse_args().config_path

    with open(config_path, 'r') as f:
        config_string = '[dummy_section]\n' + f.read()  # configparser requires to have sections
    config = configparser.ConfigParser()
    config.read_string(config_string)

    cs = config['dummy_section']  # config section
    return cs['tg_username'], cs['tg_bot_token'], cs['hostname']


if __name__ == '__main__':
    username, tg_secret, hostname = parse_args()

    updater = Updater(token=tg_secret)
    dispatcher = updater.dispatcher

    def check_user(_, update):
        if update.message.from_user.username != username:
            raise DispatcherHandlerStop

    dispatcher.add_handler(MessageHandler(Filters.all, check_user), group=-1)

    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(CommandHandler('newkey', new_key))

    dispatcher.add_handler(MessageHandler(Filters.text, partial(bash, hostname=hostname)))

    updater.start_polling()
