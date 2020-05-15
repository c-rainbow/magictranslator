import unittest

import storage



class StorageTest(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.storage = storage.Storage()

    def testEncryption(self):
        message = 'Test message1234'
        encrypted = self.storage.Encrypt(message)
        decrypted = self.storage.Decrypt(encrypted)
        self.assertEqual(message, decrypted.decode('utf8'))


if __name__ == '__main__':
    unittest.main()