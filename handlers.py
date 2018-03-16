from key_gen import get_public_save_private_key
from time import sleep
import paramiko
import threading

FILE_SECRET = 'private.key'
LINES_PER_MSG = 10

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='still under development')


def new_key(bot, update):
    public = get_public_save_private_key(file_secret=FILE_SECRET)
    bot.send_message(chat_id=update.message.chat_id, text=public.decode('utf-8'))


# class Buffer:
#     def __init__(self, stdout, bot, timeout=.25):
#         self.bot = bot
#         self._buffer = []
#         self.timeout=timeout
#
#
#     t = threading.Thread(target=task, args=(data,))
#     t.start()
#
#     def cycle_post(self):
#         while True:
#             if len(self._buffer) != 0:
#                 self.bot.send_message(chat_id=update.message.chat_id)
#
#             if len(self._buffer) == 0:
#                 return
#
#     def flush(self):
#         self.bot.send_message(chat_id)


def bash(bot, update):
    client = get_client()
    stdin, stdout, stderr = client.exec_command(update.message.text, get_pty=True)
    print(type(stdout))
    # lines = stdout.readlines()
    # bot.send_message(chat_id=update.message.chat_id, text=''.join(lines))

    print('chat_id', update.message.chat_id)

    buffer = []
    for i, line in enumerate(iter(stdout.readline, '')):
        buffer.append(line)
        if len(buffer) == LINES_PER_MSG:
            bot.send_message(chat_id=update.message.chat_id, text=''.join)
        print('iteration')
        bot.send_message(chat_id=update.message.chat_id, text=''.join(lines))
        sleep(0.25)
    print('here')
    print(update.message.chat_id)
    bot.send_message(chat_id=update.message.chat_id, text='### finished')
    print('here2')
    client.close()


def get_client():
    key = paramiko.RSAKey(filename=FILE_SECRET)
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    hostname = 'cb.skoltech.ru'
    client.get_host_keys().add(hostname, 'ssh-rsa', key)
    client.connect(hostname=hostname)
    return client
