from security import get_public_save_private_key, get_client
from time import sleep
from collections import deque
import threading
from telegram.ext.dispatcher import run_async


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Hello.')


def new_key(bot, update):
    public = get_public_save_private_key()
    bot.send_message(chat_id=update.message.chat_id, text=public.decode('utf-8'))


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
    client_holder[0].close()
    client_holder[0] = get_client(hostname=hostname)
    bot.send_message(chat_id=update.message.chat_id, text='### connection was reestablished')


@run_async
def shell(bot, update, client_holder):
    _, stdout, _ = client_holder[0].exec_command(update.message.text, get_pty=True)
    buffer = Buffer(bot, update.message.chat_id)
    for i, line in enumerate(iter(stdout.readline, '')):
        buffer.append(line)
    buffer.close()
    bot.send_message(chat_id=update.message.chat_id, text='### finished')
