from flask import Flask
from flask import render_template, request
import json
import urllib.request
import re
import os

app = Flask(__name__)

def weather():
    req = urllib.request.Request('https://yandex.ru/pogoda/skopje')
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    regWeather = re.compile('<span class="temp__value">.*?</span>', flags= re.DOTALL)
    weather = regWeather.findall(html)
    regTag = re.compile('<.*?>', re.DOTALL)
    temp = regTag.sub("", weather[0])
    return(temp)


def dictionary():
    f = open('dictionary.csv','r',encoding = 'UTF-8')
    lines = f.readlines()
    dic = {}
    for l in lines:
        words = l.replace('\n', '')
        w = words.split('\t')
        if '&#1123;' in w[1]:
            w[1] = w[1].replace('&#1123;','ѣ')
        if '&#1110;' in w[1]:
            w[1] = w[1].replace('&#1110;','i')
        if '&#1141;' in w[1]:
            w[1] = w[1].replace('&#1141;','ѵ')
        if '&#1139;' in w[1]:
            w[1] = w[1].replace('&#1139;','ѳ') 
        dic[w[0]] = w[1]
    dic['более'] = 'болѣе'
    return(dic)


def orthog(word):
    cons = 'БВГДЖЗКЛМНПРСТФХЦШбвгджзклмнпрстфхцш'
    vow = 'АЕЁИЙОУЫЭЮЯаеёийоуыэюя'
    for l in range(0,len(word)):
        if l < len(word)-1:
            if word[l] == 'и':
                if word[l+1] in vow:
                    word = word.replace('и', 'і')
        else:
            if word[l] in cons:
                word += 'ъ'
    if word.startswith('черес'):
        word = word.replace('черес', 'через')
    if word.startswith('бес'):
        word = word.replace('бес', 'без')
    if word.startswith('чрес'):
        word = word.replace('чрес', 'чрез')
    if word.startswith('Черес'):
        word = word.replace('Черес', 'Через')
    if word.startswith('Бес'):
        word = word.replace('Бес', 'Без')
    if word.startswith('Чрес'):
        word = word.replace('Чрес', 'Чрез')
    return(word)

def get_text(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('windows-1251')
    regText = re.compile('<a href.*?</a>', flags= re.DOTALL)
    text = regText.findall(html)
    regTag = re.compile('<.*?>', re.DOTALL)
    regOther = re.compile('\\n|\\t|\\r', re.DOTALL)
    clean_text = []
    for t in text:
        t2 = regTag.sub("", t)
        t3 = t2
        if (('\n' in t2) | ('\r' in t2) | ('\t' in t2)):
            t3 = regOther.sub('',t2)
        if not ((t3 == '')|(t3 == 'lowsrc()')):
            if not re.search('просмотров: [0-9]+',t3):
                if re.search('[A-Z|a-z|0-9|а-я|А-Я]',t3):
                    if re.search(' ',t3):
                        clean_text.append(t3)
    f = open('text.txt', 'w', encoding = 'UTF-8')
    for c in clean_text:
        f.write(c + '\n')
    f.close()
    os.system("C:\mystem.exe -csdig text.txt output.txt")
    return()

def dorev():
    f1 = open('text.txt', 'r', encoding = 'UTF-8')
    f2 = open('output.txt', 'r', encoding = 'UTF-8')
    dic = dictionary()
    text = f1.readlines()
    new_text = []
    words = []
    new = {}
    for line in text:
        arr = line.split()
        for a in arr:
            words.append(a)
    mystem = f2.read()
    grammar = mystem.split()
    for g in grammar:
        reg = '([а-яА-Я]+){([а-яА-Я]+)='
        r = re.search(reg,g)
        if r:
            word = r.group(1)
            lemma = r.group(2)
            flex = ''
            ending = ''
            lw = word.lower()
            if len(word)<len(lemma):
                length = len(word)
            else:
                length = len(lemma)
            for i in range(0, length):
                if lw[i] == lemma[i]:
                    flex += word[i]
            if len(flex)<len(word):
                for i in range(len(flex), len(word)):
                    ending += word[i]
            new_word = ''
            if lemma in dic:
                l = dic[lemma]
                for i in range(0, len(flex)):
                    new_word += l[i]
                new_word += ending
            else:
                new_word = word
            new_word = orthog(new_word)
            if (('S' in g) & ('ед' in g) & ('пр' in g)|('дат' in g)):
                if new_word.endswith('е'):
                    k = ''
                    for i in range(0, len(new_word)-1):
                        k += new_word[i]
                    k += 'ѣ'
                    new_word = k
            new[word] = new_word
    for line in text:
        arr = line.split()
        new_arr = []
        for a in arr:
            if a in new:
                a = new[a]
            new_arr.append(a)
        s = ' '.join(new_arr)
        new_text.append(s)
    return(new_text)


@app.route('/')
def form():
    temp = weather()
    dic = dictionary()
    if request.args:
        word = request.args['word']
        l_word = word.lower()
        if word in dic:
            new_word = dic[word]
        if l_word in dic:
            new_word = dic[l_word]
        else:
            new_word = orthog(word)
        return render_template('answer.html', new_word=new_word)
    return render_template('index.html', temp=temp)

@app.route('/news')
def news():
    get_text('https://www.kommersant.ru/')
    text = dorev()
    return render_template('news.html', text=text)

@app.route('/test')
def test():
    if request.args:
        result = 0
        mistakes = []
        res = request.args
        for r in res:
            if res[r] == 'yes':
                result += 1
            else:
                mistakes.append(r)
        return render_template('results.html', result=result, mistakes=mistakes)
    return render_template('test.html')

if __name__ == '__main__':
    app.run()
