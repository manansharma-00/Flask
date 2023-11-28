from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

#create a flask Instance
app = Flask(__name__)

# Old SQL Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/our_users'
#Secret Key!
app.config['SECRET_KEY'] = "this is an important key"
#Itinitalise a database
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favourite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #Make passwords
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    

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
    favourite_color = StringField("Fav Color")
    password_hash = 
    password_hash2 = 
    submit = SubmitField("Submit")


#Update Database Record
@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favourite_color = request.form['favourite_color']
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("update.html",
                                   form = form,
                                   name_to_update = name_to_update)
        except:
            flash("Try harder, you do errors kiddo!")
            return render_template("update.html",
                                   form = form,
                                   name_to_update = name_to_update)
    else:
        return render_template("update.html",
                                   form = form,
                                   name_to_update = name_to_update,
                                   id = id)


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    
    if form.validate_on_submit():
        user = Users.query.filter_by(email=str(form.email.data)).first()

        if user is None:
            user = Users(name=str(form.name.data), 
                         email=str(form.email.data),
                         favourite_color = str(form.favourite_color.data))
            db.session.add(user)
            db.session.commit()

        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favourite_color.data = ''
        flash("User added Successfully!")

    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", 
                           form=form, 
                           name=name, 
                           our_users=our_users)



#Delete Database Record
@app.route('/delete/<int:id>')
def delete(id):
    name = None
    form = UserForm()
    user_to_delete = Users.query.get_or_404(id)

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html", 
                           form=form, 
                           name=name, 
                           our_users=our_users)
    except:
        flash("Error, try again!")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html", 
                           form=form, 
                           name=name, 
                           our_users=our_users)




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

