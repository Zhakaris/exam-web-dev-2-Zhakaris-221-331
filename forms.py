# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, SelectMultipleField, IntegerField, FileField
from wtforms.validators import DataRequired, Length, NumberRange
from models import Genre
from datetime import datetime  # Добавьте этот импорт

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=1000, max=datetime.now().year)])
    publisher = StringField('Publisher', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    pages = IntegerField('Pages', validators=[DataRequired()])
    cover = FileField('Cover', validators=[DataRequired()])
    genres = SelectMultipleField('Genres', choices=[(g.id, g.name) for g in Genre.query.all()], validators=[DataRequired()])
    submit = SubmitField('Save')

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[
        (5, 'Excellent'),
        (4, 'Good'),
        (3, 'Satisfactory'),
        (2, 'Unsatisfactory'),
        (1, 'Poor'),
        (0, 'Terrible')
    ], coerce=int, validators=[DataRequired()])
    review_text = TextAreaField('Review Text', validators=[DataRequired()])
    submit = SubmitField('Submit Review')
