
from multitranslator import translator
from multitranslator.storage import config_storage


if __name__ == '__main__':
    storage = config_storage.ConfigStorage()
    t = translator.FromConfigStorage(storage)
    
    #res = t.Translate('ありがとうございます')
    #print(res)

    res = t.Translate('Мне подойдёт любой день')
    print(res)

    # AWS
    #res = t.Translate('hola amigo buenas noches')
    #print(res)

    # 영어 번역 안함
    res = t.Translate('hello world hello Python')
    print(res)

    # 한국어 번역 안함
    res = t.Translate('이것은 한국어입니다')
    print(res)

    # 기타 언어
    res = t.Translate('吉林舒兰急寻去过清华浴池居民')
    print(res)