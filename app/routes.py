from flask import render_template, request, redirect, abort, jsonify, make_response, url_for
from app import app, db
from app.models import Poem
from app.ml import generate_poem
from app.forms import PoemForm
import datetime
import time

VERSION = "0.3"


@app.route('/')
def main():

    form = PoemForm()

    form.seed.default = "test"
    form.process()

    return render_template("main.html", form=form)


@app.route('/generate', methods=['POST'])
def generate():

    # get things from form
    seed = request.form['seed']
    author = request.form['author'] if request.form['author'] else "PoetryAI"
    numWords = request.form['numWords'] or 100

    # prepare data for running model
    poemData = {
        "seed": seed,
        "numWords": numWords,
        "author": author
    }

    pid = addPoemToDB(poemData)

    time.sleep(2)

    return redirect('/poem/' + str(pid))


def addPoemToDB(poemData):
    # generate poem
    poemText = generate_poem(poemData=poemData)

    p = Poem(title=poemData["seed"],
             seed=poemData["seed"],
             author=poemData["author"],
             numWords=poemData["numWords"],
             text=poemText,
             timestamp=datetime.datetime.now())

    db.session.add(p)
    db.session.commit()

    return p.id


@app.route('/poem/<id>')
def poem(id):

    p = Poem.query.get(id)

    if (p is None):
        return redirect('/poem/notFound')

    poem = p

    poem = {
        'title': p.title,
        'author': p.author,
        'textArray': p.text.split("\n"),
        'seed': p.seed if p.seed else p.title,
        'numWords': p.numWords,
        'timestamp': p.timestamp.strftime("%c") if p.timestamp else "",
        'id': id,
    }

    return render_template("poem.html", poem=poem, version=VERSION)


@app.route('/api/v1.0/poem/<int:id>', methods=['GET'])
def getPoem(id):
    p = Poem.query.get(id)

    if (p is None):
        return make_response(jsonify({'error': 'Not found'}), 404)


    poem = {
        'title': p.title,
        'author': p.author,
        'text': p.text,
        'textArray': p.text.split("\n"),
        'seed': p.seed if p.seed else p.title,
        'numWords': p.numWords,
        'timestamp': p.timestamp.strftime("%c") if p.timestamp else "",
        'id': id,
        'url': url_for("poem", id=str(id))
    }

    data = {}

    data["poems"] = {}

    data["poems"][id] = poem

    return jsonify(data)


@app.route('/main')
@app.route('/index')
def returnToHome():
    return main()


@app.errorhandler(404)
def notFound(error):
    print(request.method)
    if request.method == 'GET':
        make_response(jsonify({'error': 'Not found'}), 404)
    return render_template("404.html"), 404


@app.route('/poem/notFound')
def poemNotFound():
    return render_template("404.html")


@app.route('/about')
def about():
    return render_template("about.html")
