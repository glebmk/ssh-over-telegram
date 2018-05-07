import argparse
import configparser
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, DispatcherHandlerStop
from handlers import new_key, start, cancel_signal, shell
from functools import partial
from security import get_client

import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


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
    to_return = [
        cs['tg_username'],
        cs['tg_bot_token'],
        cs.get('username', None),
        cs['hostname'],
        cs.get('port', 22)
    ]
    return to_return


if __name__ == '__main__':
    tg_username, tg_secret, username, hostname, port = parse_args()
    connection_info = (username, hostname, port)
    logger.info('Connection info:', connection_info)

    updater = Updater(token=tg_secret)
    dispatcher = updater.dispatcher

    def check_user(_, update):
        if update.message.from_user.username != tg_username:
            raise DispatcherHandlerStop

    dispatcher.add_handler(MessageHandler(Filters.all, check_user), group=-1)

    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(CommandHandler('newkey', partial(new_key)))

    client_holder = [get_client(connection_info)]

    dispatcher.add_handler(CommandHandler('c', partial(cancel_signal, client_holder=client_holder, connection_info=connection_info)))

    dispatcher.add_handler(MessageHandler(Filters.text, partial(shell, client_holder=client_holder, connection_info=connection_info)))

    updater.start_polling()
