
import langdetect


class LanguageDetector(object):

    def __init__(self, storage):
        self.storage = storage

    def Detect(self, text):
        # TODO: Improve this
        return langdetect.detect(text)

    
    
    

    