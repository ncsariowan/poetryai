from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class PoemForm(FlaskForm):
    seed = StringField('Seed Phrase', validators=[DataRequired()])
    numWords = IntegerField('Number of Words', validators=[DataRequired()])
    author = StringField('Your name (optional)')
    submit = SubmitField('Generate')