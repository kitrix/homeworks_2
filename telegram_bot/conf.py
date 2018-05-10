TOKEN = "569645248:AAEM78pFrBv6JvVIMfeSjEWnLCVDhk3Aqv8"
WEBHOOK_HOST = 'afanaseva.pythonanywhere.com'
WEBHOOK_PORT = '443'

def change(message):
    import re
    import random
    from pymorphy2 import MorphAnalyzer
    morph = MorphAnalyzer()

    # открытие и чтение
    def open_and_read():
        f = open("text.txt", 'r', encoding="utf-8")
        s = f.read()
        f.close()
        return s

    # предобработка текста
    punct = '[.,!«»?&@"$\[\]\(\):;%#&\'—-]'

    def preprocessing(text):  # функция предобработки текста
        text_wo_punct = re.sub(punct, '', text.lower())  # удаляем пунктуацию, приводим в нижний регистр
        words = text_wo_punct.strip().split()  # делим по пробелам
        return words

    text = open_and_read()
    words = preprocessing(text)
    # print(words)

    s = message
    print(s)
    reply = ''
    mes = preprocessing(s)
    for m in mes:
        f = morph.parse(m)[0]
        l = f.normalized
        t = l.tag
        inf = f.tag
        if 'PREP' in f.tag or 'NPRO' in f.tag:
            reply += f.word + ' '
            continue
        inf_tags = str(inf).split(',')
        lem_tags = str(t).split(',')
        new_inf = []
        for i in inf_tags:
            if i not in lem_tags:
                new_inf.append(i)
        if new_inf != []:
            for i, tag in enumerate(new_inf):
                if ' ' in tag:
                    d = re.sub('[A-Za-z]+ ', '', tag)
                    new_inf[i] = d
        count = 0
        while True:
            count += 1
            if count > 1000:
                break
            w = random.choice(words)
            first = morph.parse(w)[0]
            lemma = first.normalized
            tags = lemma.tag
            if t == tags:
                if new_inf != []:
                    new = first.inflect(set(new_inf))
                    n = new.word
                    reply += n + ' '
                else:
                    reply += lemma.word + ' '
                break
    return(reply)
