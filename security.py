from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
import paramiko
from paramiko.ssh_exception import BadHostKeyException, SSHException
import os
import logging

PRIVATE_KEY = 'private.key'
HOST_KEY = 'host.key'
logger = logging.getLogger()


def get_public_save_private_key(file_secret=PRIVATE_KEY):
    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=2048
    )

    public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    )

    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.TraditionalOpenSSL,
        crypto_serialization.NoEncryption())

    with open(file_secret, 'wb') as f:
        f.write(private_key)

    os.chmod(file_secret, 0o0600)  # Set read and write permission for user only

    return public_key


def save_host_key(hostname, file_secret=HOST_KEY):
    os.system(f'ssh-keyscan {hostname} > {file_secret}')


def get_client(hostname):
    if not os.path.exists(PRIVATE_KEY) or not os.path.exists(HOST_KEY):
        return None
    client = paramiko.SSHClient()
    client.get_host_keys().load(HOST_KEY)

    try:
        client.connect(hostname=hostname, key_filename=PRIVATE_KEY, allow_agent=False, look_for_keys=False)
    except (BadHostKeyException, SSHException):
        logger.error(msg='Cannot establish connection', exc_info=True)
        return None
    return client
