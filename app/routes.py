from flask import render_template, request, redirect
from app import app, db
from app.models import Poem
from app.ml import generate_poem

@app.route('/')
def main():
    return render_template("main.html")

@app.route('/generate', methods = ['POST'])
def generate():
    root = request.form['root']
    name = request.form['name'] if request.form['name'] else "PoetryAI"
    numWords = request.form['number']

    poemData = {
        "root": root,
        "numWords": numWords
    }

    #generate poem
    poemText = generate_poem(poemData=poemData)

    p = Poem(title=root, author=name, numWords=numWords, text="Poetry is cool\nI really like this poem\nThank you for reading")
    db.session.add(p)
    db.session.commit()


    return redirect('/poem/' + str(p.id))

@app.route('/poem/<id>')
def profile(id):

    p = Poem.query.get(id)
    
    if (p is None):
        return redirect('/poem/notFound')

    poem = {
        'title': p.title,
        'author': p.author,
        'text': p.text.split("\n")
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