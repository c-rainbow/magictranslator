
import requests
import unittest
from unittest import mock

from magictranslator.translators import yandex_api


class YandexAPITests(unittest.TestCase):
    
    @mock.patch.object(requests, 'post')
    def testTranslate(self, post_mock):
        post_mock.return_value.text = '{ "lang": "la-ru", "text": ["Cogito, ergo sum"]}'

        translator = yandex_api.YandexTranslator('test_api_key')
        response = translator.Translate('Я мыслю, следовательно, я есмь', 'la', 'ru')
        self.assertEqual('Я мыслю, следовательно, я есмь', response.original_text)
        self.assertEqual("Cogito, ergo sum", response.translated_text)
        self.assertEqual('la', response.src)
        self.assertEqual('ru', response.dest)
        self.assertEqual('yandex', response.translator)
        self.assertIsNone(response.error)

        expected_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=test_api_key&lang=la-ru'
        post_mock.assert_called_once_with(expected_url, data={'text': 'Я мыслю, следовательно, я есмь'})


if __name__ == '__main__':
    unittest.main()
