import re
import urllib.request
import requests

def get_urls():
    page = requests.get('http://www.dorev.ru/ru-index.html') 
    page.encoding = 'windows-1251'
    html = page.text
    #req = urllib.request.Request('http://www.dorev.ru/ru-index.html')
    #with urllib.request.urlopen(req) as response:
        #html = response.read().decode('utf-8')
    regUrls = re.compile('<a href="ru-index\.html.*?>', flags= re.DOTALL)
    urls = regUrls.findall(html)
    clear_url = []
    for u in urls:
        url = u.replace('<a href="', '')
        url2 = url.replace('">','')
        clear_url.append('http://www.dorev.ru/' + url2)
    return(clear_url)

def make_dictionary(urls):
    f = open("dictionary.csv", 'w', encoding = "utf-8")
    for url in urls:
        page = requests.get(url) 
        page.encoding = 'windows-1251'
        html = page.text
        #req = urllib.request.Request(url, headers={'User-Agent':user_agent})
        #with urllib.request.urlopen(req) as response:
            #html = response.read().decode('windows-1251')
        regWords = re.compile('<tr valign="top" bgcolor="#.*?">.*?</tr>', flags= re.DOTALL)
        words = regWords.findall(html)
        words2 = []
        for word in words:
            word2 = word.replace('<td class="uu">','<td class="uu">@@@')
            words2.append(word2)
        regTag = re.compile('<.*?>', re.DOTALL)
        regAt = re.compile('@@@.*?&nbsp;@@@',re.DOTALL)
        clear_words = []
        for w in words2:
            w2 = regTag.sub("",w)
            w3 = regAt.sub("",w2)
            w4 = w3.replace("'", '')
            clear_words.append(w4)
        regWords = '([а-яА-ЯЁё-]*)@@@([а-яА-ЯЁё&#0-9;-]*)'
        dic = {}
        for a in clear_words:
            r = re.search(regWords, a)
            if r:
                word1 = r.group(1)
                word2 = r.group(2)
                dic[word1] = word2
        for d in sorted(dic):
            if dic[d].endswith('&'):
                dic[d] = dic[d][0:-1]
        for word in sorted(dic):
            if (('&#1110;' in dic[word])|('&#1123;' in dic[word])|\
                ('&#1141'in dic[word])|('&#1139;' in dic[word])):
                s = word + '\t' + str(dic[word]) + '\n'
                f.write(s)
    f.close()
    return()

def main():
    urls = get_urls()
    make_dictionary(urls)
    return()

main()

