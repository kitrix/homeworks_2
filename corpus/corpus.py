import urllib.request
import re
import os

def GetUrl(text):
    regPostTitle = re.compile('<h2 class="entry-title">.*?</h2>', flags= re.DOTALL)
    titles = regPostTitle.findall(text)
    artUrl = []
    for t in titles:
        regLink = '"(http.*/)"'
        toSearch = re.search(regLink,t)
        if toSearch:
            link = toSearch.group(1)
            artUrl.append(link)
    return(artUrl)


def GetArtUrl():
    url = 'http://smi67.ru/date/'
    year = 2017
    articlesUrl = []
    while True:
        pageUrl = url + str(year)
        try:
            page = urllib.request.urlopen(pageUrl)
            text = page.read().decode('ISO-8859-1')
            articles = GetUrl(text)
            for a in articles:
                articlesUrl.append(a)
            print(pageUrl)
            i = 2
            while i<3:
                newurl = pageUrl + '/page' + str(i)
                try:
                    page2 = urllib.request.urlopen(newurl)
                    text = page2.read().decode('ISO-8859-1')
                    articles = GetUrl(text)
                    for a in articles:
                        articlesUrl.append(a)
                    print(newurl)
                except:
                    print('Error at', newurl)
                    break
                i += 1
        except:
            print('Error at', pageUrl)
            break
        year -= 1
    return(articlesUrl)  


def GetAuthor(text):
    regAuthor = re.compile('<span class="author vcard">.*?</span>', flags= re.DOTALL)
    author = regAuthor.findall(text)
    regTag = re.compile('<.*?>', re.DOTALL)
    regSpace = re.compile('\s{2,}', re.DOTALL)
    new_author = []
    for auth in author:
        clean_auth = regSpace.sub("", auth)
        clean_auth = regTag.sub("", clean_auth)
        new_author.append(clean_auth)
        au = new_author[0]
        if au == 'smi67':
            au = 'Noname'
    return(au)

def GetHeader(text):
    regHeader = re.compile('<h1 class="entry-title">.*?</h1>', flags= re.DOTALL)
    header = regHeader.findall(text)
    reg_name = '"(.)"'
    regTag = re.compile('<.*?>', re.DOTALL)
    regSpace = re.compile('\s{2,}', re.DOTALL)
    name = []
    for h in header:
        clean_header = regSpace.sub("", h)
        clean_header = regTag.sub("", clean_header)
        name.append(clean_header)
    return(name[0])

def GetDate(text):
    regDate = re.compile('<time class="entry-date published.*".*?</time>', flags= re.DOTALL)
    date = regDate.findall(text)
    regTag = re.compile('<.*?>', re.DOTALL)
    regSpace = re.compile('\s{2,}', re.DOTALL)
    new_date = []
    for d in date:
        clean_date = regSpace.sub("", d)
        clean_date = regTag.sub("", clean_date)
        new_date.append(clean_date)
    n = new_date[0]
    n = n[0:10]
    return(n)


def GetText(text):
    regText = re.compile('<p>.*?</p>', flags= re.DOTALL)
    art = regText.findall(text)
    if  art == []:
        regText = re.compile('<p style="text-align: justify;">.*?</p>', flags= re.DOTALL)
        art = regText.findall(text)
    regTag = re.compile('<.*?>', re.DOTALL)
    regSpace = re.compile('\s{2,}', re.DOTALL)
    new_text = []
    for a in art:
        clean_text = re.sub('\xa0', "",a)
        clean_text = regSpace.sub("", clean_text)
        clean_text = regTag.sub("", clean_text)
        new_text.append(clean_text)
    article = ' '.join(new_text)
    return(article)

def create_file(url):
    page = urllib.request.urlopen(url)
    text = page.read().decode('utf-8')
    author = GetAuthor(text)
    header = GetHeader(text)
    date = GetDate(text)
    year = date[len(date)-4:len(date)]
    month = date[len(date)-7:len(date)-5]
    article = GetText(text)
    file_text = '@au %s\n@ti %s\n@da %s\n@topic \n@url %s\n%s'
    directory = '.\\newspaper\\plain\\' + year + '\\' + month
    dir_mystem_plain = '.\\newspaper\\mystem-plain\\' + year + '\\' + month
    dir_mystem_xml = '.\\newspaper\\mystem-xml\\' + year + '\\' + month
    if not os.path.exists(directory):
        os.makedirs(directory)
    f_number = 0
    for root, dirs, files in os.walk(directory):
        for f in files:
            f_number += 1
        file_name = 'article' + str(f_number + 1) +'.txt'
        with open(os.path.join(root, file_name), 'w', encoding='utf-8') as art:
            path = os.path.join(root, file_name)
            art.write(file_text % (author, header, date, url, article))
        if not os.path.exists(dir_mystem_plain):
            os.makedirs(dir_mystem_plain)
        path_mystem = ' ' + dir_mystem_plain + '\\' + file_name
        os.system(r"C:\\mystem.exe -cdig " + path + path_mystem)
        if not os.path.exists(dir_mystem_xml):
            os.makedirs(dir_mystem_xml)
        path_mystem_xml = ' ' + dir_mystem_xml + '\\' + file_name
        os.system(r"C:\\mystem.exe -cdig --format xml " + path + path_mystem_xml)
    art.close
    row = '%s\t%s\t\t\t%s\t%s\tпублицистика\t\t\t\t\tнейтральный\tн-возраст\tн-уровень\tрегиональная\t%s\tУездные вести\t\t%s\tгазета\tРоссия\tСмоленская область\tru'
    f = open("newspaper\\metadata.csv", 'w', encoding = "utf-8")
    f.write(row % (path, author, header, date, url, year))
    f.close
    return()

articles = GetArtUrl()
for art_url in articles:
    create_file(art_url)
print('Done')
