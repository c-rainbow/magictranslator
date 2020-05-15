import langdetect
import unittest
from unittest import mock

from magictranslator.detector import detector as dt


class DetectorTests(unittest.TestCase):
    
    @mock.patch.object(langdetect, 'detect')
    def testDetect(self, detect_mock):
        detect_mock.return_value = 'mi'
        d = dt.LanguageDetector(None)
        lang_code = d.Detect('Kia Ora')

        self.assertEqual('mi', lang_code)
        detect_mock.assert_called_once_with('Kia Ora')


if __name__ == '__main__':
    unittest.main()