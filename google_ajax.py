import googletrans

import response


TRANSLATOR_NAME = 'googletrans'


def FromConfig(unused_config):
    return GoogleAjaxTranslator()


class GoogleAjaxTranslator():

    def __init__(self):
        self.translator = googletrans.Translator()

    def Translate(self, original_text, src, dest):
        translation = self.translator.translate(original_text, src=src, dest=dest)
        response = response.TranslationResponse(
            original_text, translation.text, translation.src, translation.dest, TRANSLATOR_NAME, None)
        return response
