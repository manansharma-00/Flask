from flask import Flask, render_template

#create a flask Instance
app = Flask(__name__)

#create a route decorator
@app.route('/')  #if we just want to stay at the main web page

# def index():
#     return "<h1>Hello World!</h1>"

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