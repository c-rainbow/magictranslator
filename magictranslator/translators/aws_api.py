
import boto3
from magictranslator import response


TRANSLATOR_NAME = 'aws'


def FromConfig(config):
    return AwsTranslator(config)  # AWS translator client gets all config from the environment.


class AwsTranslator(object):

    def __init__(self, config):
        region_name = config.get('region')
        self.translator = boto3.client(service_name='translate', region_name=region_name, use_ssl=True)

    def Translate(self, original_text, src, dest):
        result = self.translator.translate_text(
            Text=original_text, SourceLanguageCode=src, TargetLanguageCode=dest)
        translated_text = result.get('TranslatedText')
        src_code = result.get('SourceLanguageCode')
        dest_code = result.get('TargetLanguageCode')
        return response.TranslationResponse(
            original_text, translated_text, src_code, dest_code, TRANSLATOR_NAME, None)
