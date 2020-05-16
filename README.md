Wrapper library of multiple translation APIs.

With this library, you can configure the following:
(1) For each source language, which translation API to use
(2) For each source language, which destination language to translate to

Config JSON file structure

MagicTranslator accepts JSON-like data as input config. The config JSON file
(as shown in config.json) has the following structure

"translators": {
    List translators to use, with credentials (API key, etc)
    Each translator has name (which should match the names in the Python file), and optional credential info.
    The list of currently supported translator names are: googletrans, google, aws, yandex

}


"default_translator": which translator to use by default, when the source language is not configured in src_langs. The name should be one of the translators in "translators" section

"default_dest": to which language to translate by default. Should be a valid ISO-639-1 two-character code

"no_translates": languages not to translate. Should be a valid ISO-639-1 two-character code


"src_langs": source languages. Each object in the list has three fields
"src" (required) ISO-639-1 code of the source language
"dest" (optional) ISO-639-1 code of the destination language. If missing, default_dest is used
"translator" (optional) name of translator to use. The name should be one of the translators in "translators" section


Usage

[code]

from magictranslator import translator

t = translator.FromJSONConfigFile('config.json')  
res = t.Translate('hola amigo buenas noches')
print(res.translated_text)

[/code]

