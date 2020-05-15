
import base64
import json
import os
import pathlib

from Crypto import Random
from Crypto.Cipher import AES


AES_BLOCK_SIZE = 32  # 256 bits
_INITIALIZATION_VECTOR = b'1234567890123456'
_MODE = AES.MODE_CBC
_PADDING_CHAR = ' '

_IS_ENCRYPTED_KEY = 'is_encrypted'
_PADDING_KEY = 'padding'
_CONTENT_KEY = 'content'
_UTF8 = 'utf8'


class Crypto(object):

    def __init__(self, aes_key=None, iv=_INITIALIZATION_VECTOR):
        self.aes_key = aes_key
        if self.aes_key:
            self.encryptor = AES.new(self.aes_key, _MODE, iv)
            self.decryptor = AES.new(self.aes_key, _MODE, iv)

    def ReadAESFile(self):
        aes_file = pathlib.Path(self.aes_filepath)
        if not aes_file.exists():
            return None
        with open(aes_file, 'rb') as fp:
            aes_key = fp.read()
        return aes_key

    def GenerateNewAESKey(self):
        return Random.get_random_bytes(AES_BLOCK_SIZE)

# Append padding to data before encryption
def PadData(content):
    # Assumes that content is str to encrypt
    content_bytes = content.encode(_UTF8)
    rem = len(content_bytes) % AES_BLOCK_SIZE
    if rem > 0:
        padding = _PADDING_CHAR * (AES_BLOCK_SIZE - rem)
        return (content + padding).encode(_UTF8), padding
    return content_bytes, ''


# Traverse json-like data and encrypt where necessary
def EncryptRecursively(data, encryptor):
    data_type = type(data)
    if data_type == list:
        return [EncryptRecursively(elem, encryptor) for elem in data]

    if data_type == dict:
        if _IS_ENCRYPTED_KEY in data and data[_IS_ENCRYPTED_KEY] is False:
            new_data = dict(data)
            padded_data, padding = PadData(new_data[_CONTENT_KEY])
            new_data[_IS_ENCRYPTED_KEY] = True
            new_data[_PADDING_KEY] = padding
            new_data[_CONTENT_KEY] = base64.b64encode(encryptor.encrypt(padded_data)).decode(_UTF8)
            return new_data
        return {key: EncryptRecursively(value, encryptor) for key, value in data.items()}

    return data


# Traverse json-like data and decrypt where necessary
def DecryptRecursively(data, decryptor):
    data_type = type(data)
    if data_type == list:
        return [DecryptRecursively(elem, decryptor) for elem in data]

    if data_type == dict:
        if data.get(_IS_ENCRYPTED_KEY):
            new_data = dict(data)
            decrypted = base64.b64decode(data[_CONTENT_KEY])
            decrypted = decryptor.decrypt(decrypted).decode(_UTF8)
            new_data[_IS_ENCRYPTED_KEY] = False
            new_data[_CONTENT_KEY] = decrypted[:-len(data[_PADDING_KEY])]
            return new_data
        return {key: DecryptRecursively(value, decryptor) for key, value in data.items()}

    return data
