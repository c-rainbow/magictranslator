import collections


TranslationResponse = collections.namedtuple(
    'TranslationResponse', ['original_text', 'translated_text', 'src', 'dest', 'translator', 'error']
)
