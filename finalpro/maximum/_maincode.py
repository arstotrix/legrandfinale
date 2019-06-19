from flask import Flask, render_template, request
import urllib.request
import json
from pymystem3 import Mystem
import pymorphy2
import collections

def getsearcher(link, word):
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
    while of < total:
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
            # print(post['date'], post['text'])
            text = post['text']
            lemmas = m.lemmatize(text)
            # print(lemmas)
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
        for lemma in texts[text]:
            x = text
            y = 0
            if word == lemma:
                y = texts[text][lemma]
            xs.append(x)
            ys.append(y)
    X = []
    Y = []
    results = {}
    for i, x in enumerate(xs):
        results[x] = ys[i]
    od = collections.OrderedDict(sorted(results.items()))
    for o in od:
        X.append(o)
        Y.append(od[o])
    return X, Y

def plott(X,Y):
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graph', methods = ['POST', 'GET'])
def graph():
    if request.method == 'POST':
        link = request.form['link']
        word = request.form['word']
        plott(getsearcher(link, word))
        fin_form = link+'\n'+word
    return render_template('graph.html', fin_form=fin_form)

if __name__ == "__main__":
    app.run(debug=False)




