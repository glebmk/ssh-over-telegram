from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
import paramiko
from paramiko.ssh_exception import BadHostKeyException, SSHException
import os
import logging

PUBLIC_KEY = 'public.key'
PRIVATE_KEY = 'private.key'
logger = logging.getLogger()


def get_public_save_private_key():
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

    with open(PUBLIC_KEY, 'wb') as f:
        f.write(public_key)

    with open(PRIVATE_KEY, 'wb') as f:
        f.write(private_key)

    # Set read and write permission for user only
    os.chmod(PUBLIC_KEY, 0o0600)
    os.chmod(PRIVATE_KEY, 0o0600)

    return public_key


def get_client(connection_info):
    if not os.path.exists(PRIVATE_KEY):
        return None
    client = paramiko.SSHClient()

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # TODO change it in future updates

    try:
        username, hostname, port = connection_info
        client.connect(username=username, hostname=hostname, port=port, key_filename=PRIVATE_KEY, allow_agent=False, look_for_keys=False)
    except (BadHostKeyException, SSHException):
        logger.error(msg='Cannot establish connection', exc_info=True)
        return None
    return client
