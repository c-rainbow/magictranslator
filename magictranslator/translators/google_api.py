
import json 

from google.cloud import translate
from google.oauth2 import service_account

from magictranslator import response

TRANSLATOR_NAME = 'google'


def FromConfig(config):
    json_file = config['service_account']
    with open(json_file, 'rb') as fp:
        data = fp.read()
    loaded = json.loads(data)
    project_id = loaded['project_id']
    return GoogleTranslator(json_file, project_id)


class GoogleTranslator(object):
    def __init__(self, credential_file, project_id):
        credentials = service_account.Credentials.from_service_account_file(credential_file)
        self.client = translate.TranslationServiceClient(credentials=credentials)
        self.parent = self.client.location_path(project_id, 'global')

    def Translate(self, original_text, src, dest):
        api_response = self.client.translate_text(
            parent=self.parent,
            contents=[original_text],
            mime_type='text/plain',
            source_language_code=src,
            target_language_code=dest,
        )

        translated_text = api_response.translations[0].translated_text
        resp = response.TranslationResponse(original_text, translated_text, src, dest, TRANSLATOR_NAME, None)
        return resp
