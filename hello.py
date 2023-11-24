from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#create a flask Instance
app = Flask(__name__)

# Old SQL Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost/our_users'
#Secret Key!
app.config['SECRET_KEY'] = "this is an important key"
#Itinitalise a database
db = SQLAlchemy(app)

#Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #Create a String
    def __repr__(self):
        return '<Name %r>' % self.name

#Create a new Flask Form
class NameForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Create a User Form
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")





# def index():
#     return "<h1>Hello World!</h1>"
#create a route decorator
@app.route('/')  #if we just want to stay at the main web page
def index():
    first_name = "john"
    stuff = "that was a great code, where did <strong>you</strong> learn it?"
    pizza = ['pepperoni','mushroom','onion',2]
    return render_template("index.html", 
                           first_name=first_name, 
                           stuff=stuff,
                           pizza=pizza)

#localhost:5000/user/name
@app.route('/user/<name>')

# def user(name):
#     return "Heloo {}!!!".format(name)

def user(name):
    return render_template("user.html", user_name = name)




#safe tag -
#when generating html from templates, there's risk that variables might include
#symbols that affect the resulting html, so to automatically escape everything
#by default, we use {{ .....| safe}}

#striptags - 
#it will remove any html tags which are present

#title - 
#capitalize first letter of each word

#trim - 
#remove trailing spaces from the end



#Custom Error pages

#Invalid URL error
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

#creating a name page
@app.route('/name', methods = ['GET','POST'])
def name():
    name = None
    form = NameForm()


    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully")
    
    return render_template("name.html",
                           name = name,
                           form = form)


@app.route('/user/add', methods=['GET','POST'])
def add_user():
    name=None
    form=UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name=form.name.data
        form.name.data=''
        form.email.data=''
        flash("User added Successfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html",
                           form=form,
                           name=name,
                           our_users=our_users)