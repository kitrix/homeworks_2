import urllib.request
import json
import matplotlib.pyplot as plt

def word_count(s):  #считает число слов
    s1 = s.lower()
    a = s1.split()
    for i, word in enumerate(a):
        a[i] = word.strip('.,!?();:*/\|<>-_%&#№@+~—"«»^')
        if a[i] == '':
            del a[i]
    result = 0
    for word in a:
        result += 1
    return result

def age_count(s):
    a = s.split('.')
    if (len(a)) > 2:
        day = a[0]
        month = a[1]
        year = a[2]
        cday = 22
        cmonth = 4
        cyear = 2018
        if int(month) <= int(cmonth):
            if int(day) <= int(cday):
                age = int(cyear) - int(year)
        else:
            age = int(cyear) - int(year) - 1
            return(age)

def av_dic(dic): #создает словарь со средними значениями
    new_dic = {}
    for d in dic:
        sum = 0
        for k in range(0, len(dic[d])):
            sum += dic[d][k]
        av = sum / len(dic[d])
        if av != 0:
            new_dic[d] = av
    return new_dic

num = 0
cities = {}
ages = {}
posts = {}
f = open("posts.txt", 'w', encoding = "utf-8")
f2 = open("comments.txt", 'w', encoding = "utf-8")

while True:
    if num >= 120:
        break
    req = urllib.request.Request('https://api.vk.com/method/wall.get?owner_id=-29534144&offset={}&count=10&v=5.74&access_token=a4cc7c41a4cc7c41a4cc7c41fea4ae5039aa4cca4cc7c41fe170755318572c5654e8cba'.format(str(num)))
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    data = json.loads(result)
    for i in range (0,10):
        post_text = data['response']['items'][i]['text'] #текст поста
        f.write(post_text + '\n')
        len_post = word_count(post_text) #длина поста
        num += 1 #счетчик постов
        post_id = data['response']['items'][i]['id']
        com_num = 0 #счетчик комментариев
        all_com = 0   #суммарная длина всех комментариев
        comm_count = data['response']['items'][i]['comments']['count']
        if comm_count > 120:
            comm_count = 120
        while True:
            if com_num >= comm_count:
                break
            req_comment = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id=-29534144&post_id={}&count=10&offset={}&v=5.74&access_token=a4cc7c41a4cc7c41a4cc7c41fea4ae5039aa4cca4cc7c41fe170755318572c5654e8cba'.format(post_id, com_num))
            response = urllib.request.urlopen(req_comment)
            result = response.read().decode('utf-8')
            data2 = json.loads(result)
            count = len(data2['response']['items'])
            for j in range(0, count):
                com_num += 1
                if 'response' in data2:
                    comment_text = data2['response']['items'][j]['text']
                    f2.write(comment_text + '\n')
                    len_comment = word_count(comment_text)
                    profile_id = data2['response']['items'][j]['from_id']
                    if profile_id > 0:
                        req_profile = urllib.request.Request('https://api.vk.com/method/users.get?user_id={}&fields=bdate,city&v=5.74&access_token=a4cc7c41a4cc7c41a4cc7c41fea4ae5039aa4cca4cc7c41fe170755318572c5654e8cba'.format(profile_id))
                        response = urllib.request.urlopen(req_profile)
                        result = response.read().decode('utf-8')
                        data_p = json.loads(result)
                        if 'bdate' in data_p['response'][0]:
                            age = age_count(data_p['response'][0]['bdate'])
                            if age:
                                if age in ages:
                                    ages[age].append(len_comment)
                                else:
                                    ages[age] = [len_comment]
                        if 'city' in data_p['response'][0]:
                            if data_p['response'][0]['city'] != '':
                                city = data_p['response'][0]['city']['title']
                                if city in cities:
                                    cities[city].append(len_comment)
                                else:
                                    cities[city] = [len_comment]
                        all_com += len_comment

        if com_num != 0:
            if len_post in posts:
                posts[len_post].append(all_com/com_num)
            else:
                posts[len_post] = [all_com/com_num]



new_c = {}
new_p = {}
new_a = {}
new_c = av_dic(cities)
new_p = av_dic(posts)
new_a = av_dic(ages)


city_nums = [new_c[city] for city in sorted(new_c)]
city_labs = [city for city in sorted(new_c)]
plt.bar(range(len(city_labs)), city_nums)
plt.title('Средняя длина комментария для разных городов')
plt.ylabel('Длина комментария')
plt.xlabel('Город')
plt.xticks(range(len(city_labs)), city_labs, rotation=90)
plt.show()

age_nums = [new_a[a] for a in sorted(new_a)]
age_labs = [a for a in sorted(new_a)]
plt.bar(range(len(age_labs)), age_nums)
plt.title('Средняя длина комментария для разных возрастов')
plt.ylabel('Длина комментария')
plt.xlabel('Возраст')
plt.xticks(range(len(age_labs)), age_labs, rotation=90)
plt.show()

post_nums = [new_p[p] for p in sorted(new_p)]
post_labs = [p for p in sorted(new_p)]
plt.bar(range(len(post_labs)), post_nums)
plt.title('Соотношение средней длины поста со средней длиной комментария')
plt.ylabel('Длина комментария')
plt.xlabel('Длина поста')
plt.xticks(range(len(post_labs)), post_labs, rotation=90)
plt.show()

f.close()
f2.close()
