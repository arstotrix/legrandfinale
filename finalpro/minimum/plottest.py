import urllib.request, json
from pymystem3 import Mystem
import pymorphy2

link = input('Введите ссылку на сообщество, например typical_olimp')
word = input('Введите слово, например, университет')
m = Mystem()

tok = 'a7fe1623a7fe1623a7fe162351a797aadeaa7fea7fe1623fb5959690245101b2b598172'
posts = []
of = 100
http = 'https://api.vk.com/method/wall.get?domain=%s&count=100&v=5.92&access_token=%s' % (link, tok)
req = urllib.request.Request(http)
response = urllib.request.urlopen(req)
result = response.read().decode('utf-8')
data = json.loads(result)
total = data['response']['count']
posts += data['response']['items']
print(total)
while of < 1000:
    http = 'https://api.vk.com/method/wall.get?domain=%s&count=100&offset=%d&v=5.92&access_token=%s' % (
        link, of, tok)
    req = urllib.request.Request(http)
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    data = json.loads(result)
    of += 100
    posts += data['response']['items']
print(len(posts))
texts = {}
for post in posts:
    if post['text'] != '':
        #print(post['date'], post['text'])
        text = post['text']
        lemmas = m.lemmatize(text)
        #print(lemmas)
        cleanlemmas = {}
        for lemma in lemmas:
            if lemma[0] in 'йцукенгшщзхъфывапролджэячсмитьбюё':
                if lemma in cleanlemmas:
                    cleanlemmas[lemma] += 1
                else:
                    cleanlemmas[lemma] = 1
        print(cleanlemmas)
        texts[post['date']] = cleanlemmas
results = {}
xs = []
ys = []
for text in texts:
    x = text
    y = 0
    for lemma in texts[text]:
        if word == lemma:
            y = texts[text][lemma]
    xs.append(x)
    ys.append(y)
results['x'] = xs
results['y'] = ys
with open('results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)


