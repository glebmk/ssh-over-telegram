from key_gen import get_public_save_private_key
from time import sleep
from collections import deque
import paramiko
import threading

FILE_SECRET = 'private.key'
LINES_PER_MSG = 10


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Hello.')


def new_key(bot, update):
    public = get_public_save_private_key(file_secret=FILE_SECRET)
    bot.send_message(chat_id=update.message.chat_id, text=public.decode('utf-8'))


class Buffer:
    def __init__(self, bot, chat_id, timeout=.2):
        self.bot = bot
        self.chat_id = chat_id
        self._buffer = deque()
        self.timeout = timeout
        self._closed = False
        self.thread = threading.Thread(target=self._start)
        self.thread.start()

    def append(self, line):
        self._buffer.append(line)

    def close(self):
        self._closed = True
        self.thread.join()

    def _start(self):
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


def bash(bot, update):
    client = get_client()
    _, stdout, _ = client.exec_command(update.message.text, get_pty=True)
    buffer = Buffer(bot, update.message.chat_id)
    for i, line in enumerate(iter(stdout.readline, '')):
        buffer.append(line)
    buffer.close()
    bot.send_message(chat_id=update.message.chat_id, text='### finished')
    client.close()


def get_client():
    key = paramiko.RSAKey(filename=FILE_SECRET)
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    hostname = 'cb.skoltech.ru'
    client.get_host_keys().add(hostname, 'ssh-rsa', key)
    client.connect(hostname=hostname)
    return client
