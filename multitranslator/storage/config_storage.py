'''Reads config JSON file and encrypt/decrypt sensitive data in it.'''

import base64
import json
import os
import pathlib

from Crypto import Random
from Crypto.Cipher import AES


AES_BLOCK_SIZE = 16
_INITIALIZATION_VECTOR = b'1234567890123456'

_MODE = AES.MODE_CBC

_IS_ENCRYPTED_KEY = 'is_encrypted'
_PADDING_KEY = 'padding'
_CONTENT_KEY = 'content'
_UTF8 = 'utf8'


class ConfigStorage(object):
    def __init__(self, data_filepath='config.json', aes_filepath='aes'):
        self.data_filepath = data_filepath
        self.aes_filepath = aes_filepath
        
        self.aes_key = self.ReadAESFile()
        if self.aes_key is None:
            print('AES key is None')
            self.aes_key = self.GenerateNewAESKey()
            self.WriteAESFile()

        self.encryptor = AES.new(self.aes_key, _MODE, _INITIALIZATION_VECTOR)
        self.decryptor = AES.new(self.aes_key, _MODE, _INITIALIZATION_VECTOR)
        self.data = self.ReadDataFile()
        #self.EncryptDataFile()

    def ReadAESFile(self):
        aes_file = pathlib.Path(self.aes_filepath)
        if not aes_file.exists():
            return None
        with open(aes_file, 'rb') as fp:
            aes_key = fp.read()
        return aes_key

    def GenerateNewAESKey(self):
        aes_key = Random.get_random_bytes(AES_BLOCK_SIZE)
        return aes_key

    def WriteAESFile(self):
        aes_file = pathlib.Path(self.aes_filepath)
        if aes_file.exists():
            return False
        with open(aes_file, 'wb') as fp:
            fp.write(self.aes_key)
        return True

    def ReadDataFile(self):
        with open(self.data_filepath, 'rb') as fp:
            content = fp.read()
        loaded = json.loads(content)
        decrypted = DecryptRecursively(loaded, self.decryptor)
        return decrypted

    def EncryptDataFile(self):
        encrypted = EncryptRecursively(self.data, self.encryptor)
        dumped = json.dumps(encrypted, indent=2)
        with open(self.data_filepath, 'w') as fp:
            fp.write(dumped)

    def GetConfig(self):
        return self.data


# Append padding to data before encryption
def PadData(content):
    # Assumes that content is str to encrypt
    content_bytes = content.encode(_UTF8)
    rem = len(content_bytes) % AES_BLOCK_SIZE
    if rem > 0:
        padding = ' ' * (AES_BLOCK_SIZE - rem)
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
            decrypted2 = base64.b64decode(data[_CONTENT_KEY].encode('utf8'))
            print('decrypted2:', decrypted2)
            decrypted = decryptor.decrypt(decrypted2)
            print('decrypted len:', len(decrypted))
            print('decrypted heads:', decrypted[:10])
            decrypted4 = decrypted.decode(_UTF8)
            new_data[_IS_ENCRYPTED_KEY] = False
            new_data[_CONTENT_KEY] = decrypted4[:-len(data[_PADDING_KEY])]
            return new_data
        return {key: DecryptRecursively(value, decryptor) for key, value in data.items()}

    return data
