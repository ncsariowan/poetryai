from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextField,SelectField
from wtforms.validators import DataRequired


class PoemForm(FlaskForm):
    seed = TextField('The beginning/title of your poem', validators=[DataRequired()])
    numWords = IntegerField('Number of Words', validators=[DataRequired()],  default=50)
    author = StringField('Your name (optional)')
    poet = SelectField('Poet to finish your poem', choices=[('whitman','whitman'),('frost','frost'),('shakespeare','shakespeare'),('seuss','seuss'),('dickinson','dickinson')])
    submit = SubmitField('Generate')