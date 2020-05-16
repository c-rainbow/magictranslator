
import googletrans
import unittest
from unittest import mock

from magictranslator.translators import google_ajax


class GoogleAjaxTests(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.config = {'region': 'test_region'}

    @mock.patch.object(googletrans, 'Translator')
    def testTranslate(self, googletrans_mock):
        translator_mock = googletrans_mock.return_value
        translated_mock = translator_mock.translate.return_value
        translated_mock.text = 'Ciao mondo'
        translated_mock.src = 'ko'
        translated_mock.dest = 'it'

        t = google_ajax.GoogleAjaxTranslator()
        response = t.Translate('세계여 안녕', 'ko', 'it')
        self.assertEqual('세계여 안녕', response.original_text)
        self.assertEqual('Ciao mondo', response.translated_text)
        self.assertEqual('ko', response.src)
        self.assertEqual('it', response.dest)
        self.assertEqual('googletrans', response.translator)
        self.assertIsNone(response.error)


if __name__ == '__main__':
    unittest.main()