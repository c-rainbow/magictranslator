
import json

from magictranslator import response
from magictranslator.detector import detector
from magictranslator.translators import aws_api
from magictranslator.translators import google_ajax
from magictranslator.translators import google_api
from magictranslator.translators import yandex_api


def FromJSONConfigFile(config_filepath):
    with open(config_filepath, 'r') as fp:
        content = fp.read()
    config = json.loads(content)
    lang_detector = detector.LanguageDetector(config)
    translator = MagicTranslator(config, lang_detector)
    return translator


def GetTranslators(translator_configs):
    translators = dict()
    for translator_config in translator_configs:
        name = translator_config.get('name')
        
        if name == google_ajax.TRANSLATOR_NAME:
            translators[name] = google_ajax.FromConfig(translator_config)
        elif name == aws_api.TRANSLATOR_NAME:
            translators[name] = aws_api.FromConfig(translator_config)
        elif name == yandex_api.TRANSLATOR_NAME:
            translators[name] = yandex_api.FromConfig(translator_config)
        elif name == google_api.TRANSLATOR_NAME:
            translators[name] = google_api.FromConfig(translator_config)
        else:
            raise NameError('Invalid translator name: %s' % name)
    
    return translators


class MagicTranslator(object):

    def __init__(self, config, lang_detector):
        self.translators = GetTranslators(config.get('translators'))
        self.default_translator = config.get('default_translator')
        self.default_dest = config.get('default_dest')
        self.no_translates = config.get('no_translates')
        self.src_langs = config.get('src_langs')
        self.lang_detector = lang_detector

    # Gets translator and matching destination language from the source language.
    def getMatchingTranslator(self, src_code):
        if src_code in self.no_translates:
            return None, None
        for src_lang in self.src_langs:
            if src_lang.get('src') == src_code:
                translator = src_lang.get('translator', self.default_translator)
                dest_code = src_lang.get('dest', self.default_dest)
                return translator, dest_code
        
        return self.default_translator, self.default_dest

    def Translate(self, original_text, src_code=None):
        if src_code is None:
            src_code = self.lang_detector.Detect(original_text)

        translator_name, dest_code = self.getMatchingTranslator(src_code)
        if translator_name is None:  # Don't translate this language
            return response.TranslationResponse(original_text, original_text, src_code, src_code, None, None)

        translator = self.translators[translator_name]
        resp = translator.Translate(original_text, src_code, dest_code)
        return resp



