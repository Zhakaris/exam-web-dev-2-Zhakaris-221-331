from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, SelectMultipleField, SelectField, FileField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=255)])
    password = PasswordField('Password', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    middle_name = StringField('Middle Name')
    submit = SubmitField('Register')

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Description', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    publisher = StringField('Publisher', validators=[DataRequired(), Length(max=255)])
    author = StringField('Author', validators=[DataRequired(), Length(max=255)])
    pages = IntegerField('Pages', validators=[DataRequired()])
    genres = SelectMultipleField('Genres', coerce=int, validators=[DataRequired()])
    cover_id = SelectField('Cover', coerce=int, validators=[DataRequired()])
    cover = FileField('Cover Image', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])

class ReviewForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired()])
    review_text = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Add Review')

class RoleAssignmentForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    role = SelectField('Role', choices=[('1', 'Администратор'), ('2', 'Модератор'), ('3', 'Пользователь')], validators=[DataRequired()])
    submit = SubmitField('Assign Role')
