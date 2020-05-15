
from magictranslator import translator


if __name__ == '__main__':
    t = translator.FromJSONConfigFile('config.json')
    
    res = t.Translate('ありがとうございます')
    print(res)

    # Yandex test
    res = t.Translate('Мне подойдёт любой день')
    print(res)

    # AWS
    res = t.Translate('hola amigo buenas noches')
    print(res)

    # English is not translated
    res = t.Translate('hello world hello Python.')
    print(res)

    # Korean is not translated
    res = t.Translate('이것은 한국어입니다')
    print(res)

    # AWS
    res = t.Translate('吉林舒兰急寻去过清华浴池居民')
    print(res)