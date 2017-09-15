import urllib.request
req = urllib.request.Request('http://smi67.ru/')
with urllib.request.urlopen(req) as response:
   html = response.read().decode('utf-8')
import re
regPostTitle = re.compile('<h3 class="entry-title">.*?</h3>', flags= re.DOTALL)
titles = regPostTitle.findall(html)
new_titles = []
regTag = re.compile('<.*?>', re.DOTALL)
regSpace = re.compile('\s{2,}', re.DOTALL)
for t in titles:
    clean_t = regSpace.sub("", t)
    clean_t = regTag.sub("", clean_t)
    new_titles.append(clean_t)
f = open("titles.txt", 'w', encoding = "utf-8")
for t in new_titles:
    f.write(t + '\n')
f.close()
