
import requests
import unittest
from unittest import mock

from magictranslator.translators import yandex_api


class YandexAPITests(unittest.TestCase):
    
    @mock.patch.object(requests, 'post')
    def testTranslate(self, post_mock):
        post_mock.return_value.text = '{ "lang": "sv-en", "text": ["Rally to me!"]}'

        translator = yandex_api.YandexTranslator('test_api_key')
        response = translator.Translate('Alla till mig!', 'sv', 'en')
        self.assertEqual('Alla till mig!', response.original_text)
        self.assertEqual("Rally to me!", response.translated_text)
        self.assertEqual('sv', response.src)
        self.assertEqual('en', response.dest)
        self.assertEqual('yandex', response.translator)
        self.assertIsNone(response.error)

        expected_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=test_api_key&lang=sv-en'
        post_mock.assert_called_once_with(expected_url, data={'text': 'Alla till mig!'})


if __name__ == '__main__':
    unittest.main()
