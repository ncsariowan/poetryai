from app import db

class Poem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, index=True)
    author = db.Column(db.String, index=True)
    seed = db.Column(db.String)
    text = db.Column(db.String)
    numWords = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<Poem {}>'.format(self.id)