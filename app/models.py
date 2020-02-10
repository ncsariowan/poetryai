from app import db

class Poem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, index=True)
    author = db.Column(db.String, index=True)
    root = db.Column(db.String)
    text = db.Column(db.String)
    numWords = db.Column(db.Integer)

    def __repr__(self):
        return '<Poem {}>'.format(self.id)