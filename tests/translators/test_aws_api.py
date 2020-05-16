
import boto3
import unittest
from unittest import mock

from magictranslator.translators import aws_api


class AWSAPITests(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.config = {'region': 'test_region'}
    
    @mock.patch.object(boto3, 'client')
    def testTranslate(self, client_mock):
        translator_mock = client_mock.return_value
        translator_mock.translate_text.return_value = {
            'TranslatedText': "Ceci n'est pas une traduction",
            'SourceLanguageCode': 'es',
            'TargetLanguageCode': 'fr',
        }

        translator = aws_api.AwsTranslator(self.config)
        response = translator.Translate('Esto no es una traduccion', 'es', 'fr')
        self.assertEqual('Esto no es una traduccion', response.original_text)
        self.assertEqual("Ceci n'est pas une traduction", response.translated_text)
        self.assertEqual('es', response.src)
        self.assertEqual('fr', response.dest)
        self.assertEqual('aws', response.translator)
        self.assertIsNone(response.error)

        client_mock.assert_called_once_with(service_name='translate', region_name='test_region', use_ssl=True)
        translator_mock.translate_text.assert_called_once_with(
            Text='Esto no es una traduccion', SourceLanguageCode='es', TargetLanguageCode='fr')


if __name__ == '__main__':
    unittest.main()
