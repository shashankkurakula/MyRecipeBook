import re
import sqlite3
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.template_engine = "jinja2"
app.secret_key = 'your secret key'

connection = sqlite3.connect('recipes.db')
connection.execute('CREATE TABLE IF NOT EXISTS User ( id INTEGER PRIMARY KEY, firstname TEXT not null, lastname text not null, phone text not null, email TEXT NOT NULL, password TEXT NOT NULL)')
connection.execute('CREATE TABLE IF NOT EXISTS Requests ( id INTEGER PRIMARY KEY, name TEXT not null, email TEXT NOT NULL, message TEXT NOT NULL)')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/navbar')
def navbar():
    return render_template('navbar.html')

@app.route('/signin', methods=["GET", "POST"])
def signin():
    session.pop('error_message', None)
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        if not email or not password:
            session['error_message'] = 'Please fill all the fields'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            session['error_message'] = 'please enter a valid email id'
        elif not len(password) > 7:
            session['error_message'] = 'Password should contain greater than 7 characters'
        else:
            connection = sqlite3.connect('recipes.db')
            curs = connection.cursor()
            curs.execute("Select * from User where email = ?", (email, ))
            user = curs.fetchone()
            if not user:
                session['error_message'] = 'Please enter valid email & password'
            else:
                session['user_info'] = user[0]
                return render_template('index.html', user = user)
    return render_template('signin.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    session.pop('error_message', None)
    if request.method == "POST":
        fname = request.form['firstname']
        lname = request.form['lastname']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        confPass = request.form['confirmpassword']
        phone_regex = re.compile(r'^\d{3}-?\d{3}-?\d{4}$')
        if not fname or not lname or not phone or not email or not password or not confPass:
            session['error_message'] = 'Please fill all the fields'
        elif not bool(re.match(phone_regex, phone)):
            session['error_message'] = 'please enter a valid phone number'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            session['error_message'] = 'please enter a valid email id'
        elif not len(password) > 7:
            session['error_message'] = 'Password should contain greater than 7 characters'
        elif not password == confPass:
            session['error_message'] = 'Password and confirm password must be equal'
        else:
            connection = sqlite3.connect('recipes.db')
            curs = connection.cursor()
            curs.execute("Select * from User where email = ?", (email, ))
            isUserExisted = curs.fetchone()
            if not isUserExisted:
                connection = sqlite3.connect('recipes.db')
                curs = connection.cursor()
                curs.execute('Insert into User (firstname, lastname, phone, email, password) values (?, ?, ?, ?, ?)', (fname, lname, phone, email, password))
                connection.commit()
                curs.execute("Select * from User where email = ? and password = ?", (email, password))
                user = curs.fetchone()
                session['user_info'] = user[0]
                return render_template('index.html', user = user)
            else:
                session['error_message'] = 'User already exists with that email'
    return render_template('signup.html')

@app.route('/recipes')
def recipes():
    return render_template('recipes.html')

@app.route('/tags')
def tags():
    return render_template('tags.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=["GET", "POST"])
def contact():
    session.pop('request_msg', None)
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        if not name or not email or not message:
            session['error_message'] = 'Please fill all the fields'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            session['error_message'] = 'please enter a valid email id'
        else:
            connection = sqlite3.connect('recipes.db')
            curs = connection.cursor()
            curs.execute('insert into Requests (name, email, message) values(?, ?, ?)', (name, email, message))
            connection.commit()
            session.pop('error_message', None)
            session['request_msg'] = 'Request Submitted successfuly'
            return render_template('contact.html')
    return render_template('contact.html')

@app.route('/tag_template')
def tag_template():
    return render_template('tag-template.html')

@app.route('/recipes/biryani')
def biryani():
    return render_template('recipes/biryani.html')

@app.route('/recipes/mango_cake')
def mango_cake():
    return render_template('recipes/mango-cake.html')

@app.route('/recipes/spicy_shrimp')
def spicy_shrimp():
    return render_template('recipes/spicy-shrimp.html')

@app.route('/recipes/palak_dal')
def palak_dal():
    return render_template('recipes/palak-dal.html')

@app.route('/recipes/banana_ice_cream')
def banana_ice_cream():
    return render_template('recipes/banana-ice-cream.html')

@app.route('/recipes/spaghetti')
def spaghetti():
    return render_template('recipes/spaghetti.html')

@app.route('/recipes/dosa')
def dosa():
    return render_template('recipes/dosa.html')

@app.route('/recipes/dumpling_soup')
def dumpling_soup():
    return render_template('recipes/dumpling-soup.html')

@app.route('/recipes/french_onion_soup')
def french_onion_soup():
    return render_template('recipes/french-onion-soup.html')

@app.route('/signout')
def signout():
    session.pop('user_info', None)
    return redirect('/signin')

@app.route('/users')
def users():
    con = sqlite3.connect("recipes.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM User")

    rows = cur.fetchall()
    return render_template("users.html", rows=rows)

@app.route('/requests')
def requests():
    con = sqlite3.connect("recipes.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM Requests")

    rows = cur.fetchall()
    return render_template("requests.html", rows=rows)