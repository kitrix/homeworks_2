import re
from random import uniform
from collections import defaultdict
from flask import Flask
from flask import render_template, request

r_alphabet = re.compile(u'[а-яА-Яё0-9-]+|[.,:;?!]+')
r_letters = re.compile(u'[а-яА-Яё]+')

def gen_lines(corpus):
    data = open(corpus, 'r', encoding='utf-8')
    for line in data:
        yield line.lower()

def gen_tokens(lines):
    for line in lines:
        for token in r_alphabet.findall(line):
            yield token

def gen_trigrams(tokens):
    t0, t1 = '$', '$'
    for t2 in tokens:
        yield t0, t1, t2
        if t2 in '.!?':
            yield t1, t2, '$'
            yield t2, '$','$'
            t0, t1 = '$', '$'
        else:
            t0, t1 = t1, t2

def train(corpus):
    lines = gen_lines(corpus)
    tokens = gen_tokens(lines)
    trigrams = gen_trigrams(tokens)

    bi, tri = defaultdict(lambda: 0.0), defaultdict(lambda: 0.0)

    for t0, t1, t2 in trigrams:
        bi[t0, t1] += 1
        tri[t0, t1, t2] += 1

    model = {}
    for (t0, t1, t2), freq in tri.items():
        if (t0, t1) in model:
            model[t0, t1].append((t2, freq/bi[t0, t1]))
        else:
            model[t0, t1] = [(t2, freq/bi[t0, t1])]
    return model

def get_last_word(s):
    words = s.strip().split()
    last = words[len(words)-1]
    return last

def generate_sentence(model, s):
    first = get_last_word(s)
    phrase = s
    t0, t1 = '$', first
    if (t0, t1) in model:
        while 1:
            t0, t1 = t1, unirand(model[t0, t1])
            if t1 == '$': break
            if t1 in ('.!?,;:') or t0 == '$':
                phrase += t1
            else:
                phrase += ' ' + t1
    else:
        phrase = 'Cовпадений не найдено.'
    return phrase.capitalize()

def unirand(seq):
    sum_, freq_ = 0, 0
    for item, freq in seq:
        sum_ += freq
    rnd = uniform(0, sum_)
    for token, freq in seq:
        freq_ += freq
        if rnd < freq_:
            return token

app = Flask(__name__)

@app.route('/')
def index():
    model = train('harry_potter.txt')
    if request.args:
        s = request.args['input']
        if re.search(r_letters, s):
            result = generate_sentence(model, s)
            if result == 'Cовпадений не найдено.':
                return render_template('error.html', result=result)
            else:
                return render_template('result.html', result=result)
        else:
            result = 'Проверьте введенные данные!'
            return render_template('error.html', result=result)
    return render_template('index.html')

if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


