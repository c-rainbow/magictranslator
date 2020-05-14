
import boto3
import response


TRANSLATOR_NAME = 'aws'

def FromConfig(unused_config):
    return AwsTranslator()  # AWS translator client gets all config from environment.



class AwsTranslator(object):

    def __init__(self):
        self.translator = boto3.client(service_name='translate', use_ssl=True)

    def Translate(self, original_text, src, dest):
        result = self.translator.translate_text(
            Text=original_text, SourceLanguageCode=src, TargetLanguageCode=dest)
        translated_text = result.get('TranslatedText')
        src_code = result.get('SourceLanguageCode')
        dest_code = result.get('TargetLanguageCode')
        return response.TranslationResponse(original_text, translated_text, src_code, dest_code, TRANSLATOR_NAME, None)


if __name__ == '__main__':
    t = AwsTranslator()
    r = t.Translate('This is a test sentence', 'en', 'ko')
    print(r)