from security import get_public_save_private_key, get_client, save_host_key
from time import sleep
from collections import deque
import threading
from telegram.ext.dispatcher import run_async
import logging


logger = logging.getLogger()


def start(bot, update):
    logger.info('Received start command')
    text = "Hello. If you are new here or want to change your ssh key pair, run /newkey. " \
           "Please note that this command will overwrite old private key."
    bot.send_message(chat_id=update.message.chat_id, text=text)


def new_key(bot, update, hostname):
    logger.info('Received newkey command')
    public = get_public_save_private_key()
    save_host_key(hostname)
    bot.send_message(chat_id=update.message.chat_id, text=public.decode('utf-8'))
    text = "You have just received the public key. " \
           "Private key was stored in the directory from which the bot is running. " \
           "Please, add it to the authorized keys on the server. " \
           "This can be done, by appending public key to server's authorized_keys file (~/.ssh/authorized_keys)."
    bot.send_message(chat_id=update.message.chat_id, text=text)


class Buffer:
    def __init__(self, bot, chat_id, timeout=.2):
        self.bot = bot
        self.chat_id = chat_id
        self._buffer = deque()
        self.timeout = timeout
        self._closed = False
        self.thread = threading.Thread(target=self._thread_work)
        self.thread.start()

    def append(self, line):
        self._buffer.append(line)

    def close(self):
        self._closed = True
        self.thread.join()

    def _thread_work(self):
        # runs in a separate thread
        while True:
            self._send_buffer()
            if self._closed:
                return
            sleep(self.timeout)

    def _send_buffer(self):
        lines = []
        while len(self._buffer) > 0:
            lines.append(self._buffer.popleft())
        if len(lines) > 0:
            self.bot.send_message(chat_id=self.chat_id, text=''.join(lines))


@run_async
def cancel_signal(bot, update, client_holder, hostname):
    logger.info('Received cancel signal command')
    if client_holder_is_bad(bot, update, client_holder, hostname):
        return
    client_holder[0].close()
    client_holder[0] = get_client(hostname=hostname)
    bot.send_message(chat_id=update.message.chat_id, text='### connection was reestablished')


@run_async
def shell(bot, update, client_holder, hostname):
    logger.info(f'Received shell command: {update.message.text}')
    if client_holder_is_bad(bot, update, client_holder, hostname):
        return
    _, stdout, _ = client_holder[0].exec_command(update.message.text, get_pty=True)
    buffer = Buffer(bot, update.message.chat_id)
    for i, line in enumerate(iter(stdout.readline, '')):
        buffer.append(line)
    buffer.close()
    bot.send_message(chat_id=update.message.chat_id, text='### finished')


def client_holder_is_bad(bot, update, client_holder, hostname):
    if client_holder[0] is None:
        client_holder[0] = get_client(hostname)
    if client_holder[0] is None:
        logger.warning('Some problem with connection')
        bot.send_message(chat_id=update.message.chat_id, text='### some problem with the connection')
        return True
    return False
