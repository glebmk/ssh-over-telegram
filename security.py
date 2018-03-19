from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
import paramiko
import os
import logging

FILE_SECRET = 'private.key'
logger = logging.getLogger()


def get_public_save_private_key(file_secret=FILE_SECRET):
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


def get_client(hostname):
    if not os.path.exists(FILE_SECRET):
        return None
    key = paramiko.RSAKey.from_private_key_file(filename=FILE_SECRET)
    client = paramiko.SSHClient()
    client.get_host_keys().add(hostname, 'ssh-rsa', key)
    try:
        client.connect(hostname=hostname)
    except paramiko.ssh_exception.BadHostKeyException:
        logger.error('BadHostKeyException', exc_info=True)
        return None
    return client
