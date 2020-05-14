
import aws_api
import azure_api
import google_ajax
import google_api
import yandex_api


def FromConfigStorage(storage):
    config = storage.GetConfig()
    detector = detector.LanguageDetector(config)
    translator = MultiTranslator(config, detector)
    return translator


class MultiTranslator(object):

    def __init__(self, config, detector):
        self.translators = self.getTranslators(self.config)
        self.default_translator = config.get('default_translator')
        self.default_dest = config.get('default_dest')
        self.no_translates = config.get('no_translates')
        self.src_langs = config.get('src_langs')
        self.detector = detector

    def getTranslators(self, config):
        translators = dict()
        for translator_config in config.get('translators'):
            name = translator_config.get('name')
            
            if name == google_ajax.TRANSLATOR_NAME:
                translators[name] = google_ajax.FromConfig(translator_config)
            elif name == aws_api.TRANSLATOR_NAME:
                translators[name] = aws_api.FromConfig(translator_config)
            elif name == yandex_api.TRANSLATOR_NAME:
                translators[name] = yandex_api.FromConfig(translator_config)
            #elif name == google_api.TRANSLATOR_NAME:
            #    translators[name] = google_api.FromConfig(translator_config)
            #elif name == azure_api.TRANSLATOR_NAME:
            #    translators[name] = azure_api.FromConfig(translator_config)
            else:
                print('Invalid translator name:', name)
        
        return translators

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
            src_code = self.detector.Detect(original_text)

        translator_name, dest_code = self.getMatchingTranslator(src_code)
        if translator_name is None:  # Don't translate this language
            return None

        translator = self.translators[translator_name]
        response = translator.Translate(original_text, src_code, dest_code)
        return response



