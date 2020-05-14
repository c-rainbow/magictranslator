
from google.cloud import translate
from google.oauth2 import service_account
from google.oauth2 import credentials


TRANSLATOR_NAME = 'google'


def FromConfig(config):
    return None


class GoogleTranslator(object):
    def __init__(self, config):
        self.client = translate.TranslationServiceClient()
        self.parent = self.client.location_path('vivid-plateau-274207', 'global')

    def Translate(self, original_text, src, dest):
        response = self.client.translate_text(
            parent=self.parent,
            contents=[original_text],
            mime_type='text/plain',
            source_language_code=src,
            target_language_code=dest,
        )
        return response

if __name__ == '__main__':
    t = GoogleTranslator(None)
    r = t.Translate('하나 둘', 'ko', 'en')
    print(r)