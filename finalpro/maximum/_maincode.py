from flask import Flask, render_template, request
import urllib.request
import json

def getsearcher(link):
    results = {}
    return results

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graph', methods = ['POST', 'GET'])
def graph():
    if request.method == 'POST':
        link = request.form['link']
        word = request.form['word']
        results = getsearcher(link)

        fin_form = link+'\n'+word
    return render_template('graph.html', fin_form=fin_form)

if __name__ == "__main__":
    app.run(debug=False)




