from flask import render_template, request, redirect
from app import app, db
from app.models import Poem
from app.ml import generate_poem
from app.forms import PoemForm
import datetime

@app.route('/')
def main():

    form = PoemForm()

    return render_template("main.html", form=form)

@app.route('/generate', methods = ['POST'])
def generate():

    # get things from form
    seed = request.form['seed']
    author = request.form['author'] if request.form['author'] else "PoetryAI"
    numWords = request.form['numWords'] or 100

    # prepare data for running model
    poemData = {
        "seed": seed,
        "numWords": numWords 
    }

    #generate poem
    poemText = generate_poem(poemData=poemData)

    p = Poem(title=seed, seed=seed, author=author, numWords=numWords, text=poemText, timestamp=datetime.datetime.now())
    db.session.add(p)
    db.session.commit()


    return redirect('/poem/' + str(p.id))

@app.route('/poem/<id>')
def profile(id):

    p = Poem.query.get(id)
    
    if (p is None):
        return redirect('/poem/notFound')

    poem = p
    

    poem = {
        'title': p.title,
        'author': p.author,
        'text': p.text.split("\n"),
        'seed': p.seed if p.seed else p.title,
        'numWords': p.numWords,
        'timestamp': p.timestamp.strftime("%c") if p.timestamp else ""
    }

    return render_template("poem.html", poem=poem)

@app.route('/main')
@app.route('/index')
def returnToHome():
    return main()

@app.errorhandler(404)
def notFound(error):
    return render_template("404.html"), 404

@app.route('/poem/notFound')
def poemNotFound():
    return render_template("404.html")

@app.route('/about')
def about():
    return render_template("about.html")