from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from datetime import date
from wtforms.widgets import TextArea
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

#create a flask Instance
app = Flask(__name__)
bcrypt = Bcrypt(app)


# Old SQL Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/our_users'
#Secret Key!
app.config['SECRET_KEY'] = "this is an important key"
#Itinitalise a database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Form login codes...
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#Create a Login Form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password  ", validators=[DataRequired()])
    submit = SubmitField("Submit")


#Create a Login Page
@app.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username = form.username.data).first()
        if user:
            #Check the hash
            passed = bcrypt.check_password_hash(user.password_hash, form.password.data)
            if passed:
                login_user(user)
                flash("Logged in Successfully")
                return redirect(url_for('dashboard'))
            else:
                flash("Incorrect password... try again!")
        else:
            flash("Username is not registered")
    return render_template("login.html", form = form)


#Create a logout page
@app.route('/logout', methods = ['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("Logged Out Successfully")
    return redirect(url_for('login'))

#Create a Dashboard Page
@app.route('/dashboard', methods = ['GET','POST'])
@login_required  #this makes this page accesible only when the login user page has been filled
def dashboard():
    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favourite_color = request.form['favourite_color']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("dashboard.html",
                                   form = form,
                                   name_to_update = name_to_update)
        except:
            flash("Try harder!")
            return render_template("dashboard.html",
                                   form = form,
                                   name_to_update = name_to_update)
    else:
        return render_template("dashboard.html",
                                   form = form,
                                   name_to_update = name_to_update,
                                   id = id)

#Create a blog post model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default = datetime.utcnow)
    slug = db.Column(db.String(255))

#Create a posts form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget = TextArea())
    author = StringField("Author", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/posts/delete/<int:id>')
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)

    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash("Blog Post Deleted Successfully")

        #Take all the posts from the database
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts = posts)
    except:
        flash("Whoops! Looks like there's an error, try again.")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts = posts)



@app.route('/posts')
def posts():
    #Take all the posts from the database
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts = posts)

@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)  
    return render_template("post.html", post = post)

@app.route('/posts/edit/<int:id>', methods = ['GET','POST'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data

        #Update Database
        db.session.add(post)
        db.session.commit()
        flash("Post has been updated")
        return redirect(url_for('post', id = post.id))
    
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template("edit_post.html", form = form)


#Add a post page
@app.route('/add-post', methods=['GET','POST'])
# @login_required
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Posts(title = form.title.data,
                     content = form.content.data,
                     author = form.author.data,
                     slug = form.slug.data)
        #Clear the form
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''

        #Add post data to database
        db.session.add(post)
        db.session.commit()
        flash("Blog post submitted successfully")

    return render_template("add_post.html", form = form)


# A JSON page
@app.route('/date')
def get_current_date():
    favourite_pizza = {
        'john': 'pepperoni',
        'manan': 'cheese',
        'tim': 'mushroom'
    }
    return favourite_pizza
    # return {"Date": date.today()}


#Create Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable = False, unique = True)
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
    password_hash = PasswordField('Password', 
                                validators=[DataRequired(), 
                                EqualTo('password_hash2', message='Passwords Must Match!')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
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
        name_to_update.username = request.form['username']
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
            #Hash the password using bcrypt
            hashed_pw = bcrypt.generate_password_hash(form.password_hash.data).decode('utf-8')
            # hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(name=str(form.name.data), 
                         username = str(form.username.data),
                         email=str(form.email.data),
                         favourite_color = str(form.favourite_color.data),
                         password_hash = hashed_pw)
            db.session.add(user)
            db.session.commit()

        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favourite_color.data = ''
        form.password_hash.data = ''
        form.username.data = ''
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

#creating a password test page
@app.route('/test_pw', methods = ['GET','POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()


    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        #Clear the form
        form.email.data = ''
        form.password_hash.data = ''
        
        #Search User by Email Address
        pw_to_check = Users.query.filter_by(email = email).first()

        #Chech hashed password with the password we typed in the field
        # passed = check_password_hash(pw_to_check.password_hash, password) #for sha256
        passed = bcrypt.check_password_hash(pw_to_check.password_hash, password)            
    
    return render_template("test_pw.html",
                           email = email,
                           password = password,
                           pw_to_check = pw_to_check,
                           passed = passed,
                           form = form)


