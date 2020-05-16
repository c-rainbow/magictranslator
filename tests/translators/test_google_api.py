
import unittest
from unittest import mock

from google.cloud import translate
from google.oauth2 import service_account
from magictranslator.translators import google_api


class GoogleAPITests(unittest.TestCase):
    
    @mock.patch.object(translate, 'TranslationServiceClient')
    @mock.patch.object(service_account.Credentials, 'from_service_account_file')
    def testTranslate(self, credential_mock, client_mock):
        test_credential = credential_mock.return_value
        test_client = client_mock.return_value

        translated_mock = test_client.translate_text.return_value
        # The variable type in the original code is protobuf
        translated_mock.translations[0].translated_text = 'No worries'

        t = google_api.GoogleTranslator('path_to_credential_file', 'test_project_id')
        response = t.Translate('Hakuna matata', 'sw', 'en')
        self.assertEqual('Hakuna matata', response.original_text)
        self.assertEqual('No worries', response.translated_text)
        self.assertEqual('sw', response.src)
        self.assertEqual('en', response.dest)
        self.assertEqual('google', response.translator)
        self.assertIsNone(response.error)

        credential_mock.assert_called_once_with('path_to_credential_file')
        client_mock.assert_called_once_with(credentials=test_credential)
        test_client.location_path.assert_called_once_with('test_project_id', 'global')
        test_client.translate_text.assert_called_once_with(
            parent=mock.ANY, contents=['Hakuna matata'], mime_type='text/plain',
            source_language_code='sw', target_language_code='en')


if __name__ == '__main__':
    unittest.main()