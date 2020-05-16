# Magic Translator

Magic translator is a wrapper library of multiple translation APIs.

For different source languages, you can configure which translation API to use and/or which destination language to translate to.


## Config JSON file structure

MagicTranslator accepts JSON-like data config as input. The config JSON data (example can be found in config.json) has the following structure. All language codes are valid two-character ISO-639-1 codes, such as 'en', 'ar', 'ko'

### translators

List of translators to use. Each object in the list has the following items

- name (required): Name of translator. Currently supported names are: googletrans, google, aws, yandex
- optional data specific to each translator
    - googletrans: no additional data is needed
    - google: "service_account" is required with path to the service account JSON file
    - aws: "region" is required for the AWS Translate API region name
    - yandex: "api_key" is required

### default_translator

Name of the default translator. Should be one of the translators in "translators" section

### default_dest

Default destination language code to translate to

### no_translates

List of language codes not to translate

### src_langs

List of source languages to configure specifically. All other languages not in this list will be translated to default_dest by default_translator.

Each object in the list has three fields
- src (required): Source language code
- dest (optional): Destination language code, if different from default_dest
- translator (optional): Name of translator to use, if different from default_translator


## Usage

```python
from magictranslator import translator

t = translator.FromJSONConfigFile('config.json')  
res = t.Translate('hola amigo buenas noches')
print(res.translated_text)
```


