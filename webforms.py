from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField


#All the forms used in the code:

#Create a Search Form
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Create a Login Form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password  ", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Create a posts form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    # content = StringField("Content", validators=[DataRequired()], widget = TextArea())
    content = CKEditorField("Content", validators=[DataRequired()])
    author = StringField("Author")
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Create a new Flask Form
class NameForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Create a Password Form
class PasswordForm(FlaskForm):
    email = StringField("What's your email?", validators=[DataRequired()])
    password_hash = PasswordField("What's your password?", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
#Create a User Form
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favourite_color = StringField("Fav Color")
    about_author = TextAreaField("About Author")
    password_hash = PasswordField('Password', 
                                validators=[DataRequired(), 
                                EqualTo('password_hash2', message='Passwords Must Match!')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    profile_pic = FileField("Profile Pic")
    submit = SubmitField("Submit")



