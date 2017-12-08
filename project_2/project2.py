from flask import Flask
from flask import render_template, request
import json

app = Flask(__name__)


@app.route('/')
def form():
    if request.args:
        file_inp = ''
        for ans in request.args:
            file_inp += request.args[ans] + '\t'
        f = open('colors_results.csv', 'a', encoding = 'utf-8')
        f.write(file_inp)
        f.write('\n')
        f.close
        return render_template('answer.html')
    return render_template('index.html')


@app.route('/stats')
def stats():
    f = open('colors_results.csv', 'r', encoding = 'utf-8')
    lines = f.readlines()
    f.close()
    sex = {}
    age = {}
    language = {}
    city = {}
    education = {}
    for line in lines:
        arr = line.split('\t')
        if arr[0] not in sex:
            sex[arr[0]] = 1
        else:
            sex[arr[0]] += 1
        if arr[1] not in age:
            age[arr[1]] = 1
        else:
            age[arr[1]] += 1
        if arr[2] not in language:
            language[arr[2]] = 1
        else:
            language[arr[2]] += 1
        if arr[3] not in city:
            city[arr[3]] = 1
        else:
            city[arr[3]] += 1
        if arr[4] not in education:
            education[arr[4]] = 1
        else:
            education[arr[4]] += 1
    sorted_age = {}
    for key in sorted(age):
        sorted_age[key] = age[key]
    sorted_city = {}
    for key in sorted(city):
            sorted_city[key] = city[key]
    sorted_language = {}
    for key in sorted(language):
        sorted_language[key] = language[key]
    
    return render_template('stats.html',sex=sex, age=sorted_age, language=sorted_language, city=sorted_city, education=education, number=len(lines))
    

@app.route('/json')
def print_json():
    f = open('colors_results.csv', 'r', encoding = 'utf-8')
    lines = f.readlines()
    f.close
    form = []
    for line in lines:
        answers = {}
        arr = line.split('\t')
        answers['sex'] = arr[0]
        answers['age'] = arr[1]
        answers['language'] = arr[2]
        answers['city'] = arr[3]
        answers['education'] = arr[4]
        answers['color1'] = arr[5]
        answers['color2'] = arr[6]
        answers['color3'] = arr[7]
        answers['color4'] = arr[8]
        answers['color5'] = arr[9]
        form.append(answers)
    json_string = json.dumps(form, ensure_ascii=False, indent=4, separators=(',', ': '))
    return render_template('json.html', json = json_string)

    
@app.route('/search')
def search():
    if request.args:
        print(request.args)
        f = open('colors_results.csv', 'r', encoding = 'utf-8')
        lines = f.readlines()
        f.close()
        req = []
        if request.args['sex'] != "неважно":
            req.append(request.args['sex'])
        if request.args['age'] != "":
            req.append(request.args['age'])
        if request.args['lang'] != "":
            req.append(request.args['lang'])
        if request.args['city'] != "":
            req.append(request.args['city'])
        if request.args['edu'] != "неважно":
            req.append(request.args['edu'])
        result = []
       
        for line in lines:
            l = line
            for r in req:
                if r.lower() in l.lower():
                    continue
                else:
                    l = ""
            if l != "":
                result.append(l)
        print(result)
        return render_template('results.html', result=result)
    return render_template('search.html')

if __name__ == '__main__':
    app.run()
