import unittest
from unittest import mock

from magictranslator import translator as mt
from magictranslator.translators import aws_api
from magictranslator.translators import google_ajax
from magictranslator.translators import google_api
from magictranslator.translators import yandex_api

# Test 1-1. getTranslator, different combinations
# Test 1-2. getTranslator() has invalid name
# Test 2-1. getMatchingTranslator - No translation
# Test 2-2. getMT - src exists in src_langs, but missing 'translator'
# Test 2-3. getMT - src exists in src_langs, but missing 'dest'
# Test 2-4. getMT - src does not exist
# Test 3-1. Translate - no translate
# Test 3-2. Translate - translate


class MagicTranslatorTests(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.tconfig = [
            {
                'name': 'google',
                'service_account': '~/service_account.json'
            },
            {
                'name': 'aws',
                'region': 'nonexistent_region'
            },
            {
                'name': 'yandex',
                'api_key': 'trans.1.1.1.randomkey'
            },
            {
                'name': 'googletrans'
            }
        ]
        self.default_translator = 'aws'
        self.default_dest = 'fi'
        self.no_translates = ['fa', 'it']
        self.src_langs = [
            {
                'src': 'ko',
                'translator': 'google'
            },
            {
                'src': 'ru',
                'dest': 'fa',
                'translator': 'yandex'
            },
            {
                'src': 'es',
                'dest': 'ar'
            }
        ]
        self.config = {
            'translators': self.tconfig,
            'default_translator': self.default_translator,
            'default_dest': self.default_dest,
            'no_translates': self.no_translates,
            'src_langs': self.src_langs
        }

        
    # Test 1-1. getTranslator, different combinations
    @mock.patch.object(aws_api, 'FromConfig')
    @mock.patch.object(google_ajax, 'FromConfig')
    @mock.patch.object(google_api, 'FromConfig')
    @mock.patch.object(yandex_api, 'FromConfig')
    def testGetTranslators(self, *unused_mocks):
        # Test with all supported translators
        translators = mt.GetTranslators(self.tconfig)
        self.assertEqual(4, len(translators))        
        self.assertCountEqual(['google', 'aws', 'yandex', 'googletrans'], translators.keys())

        # Test with some of supported translators
        config2 = [self.tconfig[0], self.tconfig[2]]
        translators = mt.GetTranslators(config2)
        self.assertEqual(2, len(translators))
        self.assertCountEqual(['google', 'yandex'], translators.keys())

    # Test 1-2. getTranslator() has invalid name
    @mock.patch.object(aws_api, 'FromConfig')
    def testGetTranslatorsInvalidName(self, unused_mock):
        # The first translator name (AWS) is valid and should cause no error.
        config = [self.tconfig[1], {'name':'nonexistent'}]
        self.assertRaisesRegex(NameError, 'Invalid translator name: nonexistent', mt.GetTranslators, config)

    
    # Test 2-1. getMatchingTranslator - No translation
    def testGetMatchingTranslatorNoTranslate(self):
        self.config['translators'] = []
        t = mt.MagicTranslator(self.config, None)

        # Translator and dest code should be None for no-translate languages
        self.assertEqual((None, None), t.getMatchingTranslator('fa'))
        self.assertEqual((None, None), t.getMatchingTranslator('it'))
        
        # For other languages, the translator and dest code should not be None
        translator, dest_code = t.getMatchingTranslator('tr')
        self.assertIsNotNone(translator)
        self.assertIsNotNone(dest_code)

    # Test 2-2. getMatchingTranslator - src exists in src_langs, but missing 'translator'
    @mock.patch.object(aws_api, 'FromConfig')
    @mock.patch.object(google_ajax, 'FromConfig')
    @mock.patch.object(google_api, 'FromConfig')
    @mock.patch.object(yandex_api, 'FromConfig')
    def testGetMatchingTranslatorDefaultTranslator(self, *unused_mocks):
        t = mt.MagicTranslator(self.config, None)
        translator, dest_code = t.getMatchingTranslator('es')
        self.assertEqual('aws', translator)  # Default translator
        self.assertEqual('ar', dest_code)

    # Test 2-3. getMatchingTranslator - src exists in src_langs, but missing 'dest'
    @mock.patch.object(aws_api, 'FromConfig')
    @mock.patch.object(google_ajax, 'FromConfig')
    @mock.patch.object(google_api, 'FromConfig')
    @mock.patch.object(yandex_api, 'FromConfig')
    def testGetMatchingTranslatorDefaultDest(self, *unused_mocks):
        t = mt.MagicTranslator(self.config, None)
        translator, dest_code = t.getMatchingTranslator('ko')
        self.assertEqual('google', translator)
        self.assertEqual('fi', dest_code)  # Default destination language code

    # Test 2-4. getMatchingTranslator - src does not exist
    @mock.patch.object(aws_api, 'FromConfig')
    @mock.patch.object(google_ajax, 'FromConfig')
    @mock.patch.object(google_api, 'FromConfig')
    @mock.patch.object(yandex_api, 'FromConfig')
    def testGetMatchingTranslatorDefault(self, *unused_mocks):
        t = mt.MagicTranslator(self.config, None)
        translator, dest_code = t.getMatchingTranslator('newlanguage')
        self.assertEqual('aws', translator)  # Default translator 
        self.assertEqual('fi', dest_code)  # Default destination language code
    

if __name__ == '__main__':
    unittest.main()