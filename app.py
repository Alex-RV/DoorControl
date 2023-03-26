import os
import sqlite3
import requests
from flask import Flask, render_template, request, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'my_key'

def store_user(name, email, phone, pw):
    _isAdmin = 0
    door1 = 0
    door2 = 0
    conn = sqlite3.connect('./static/myapp.db')
    curs = conn.cursor()
    curs.execute("INSERT INTO users (name, email, password, phone, _isAdmin, door1, door2) VALUES((?),(?),(?),(?),(?),(?),(?))",
        (name, email, pw, phone, _isAdmin, door1, door2))

    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect('./static/myapp.db')
    curs = conn.cursor()
    all_users = [] # will store them in a list
    rows = curs.execute("SELECT * from users")  # returns as a list 

    for row in rows:# loop through all the rows.
        user = {'name' : row[0], 
                'email': row[1],
                'phone': row[2],
                'password': row[3],
                '_isAdmin' : row[4],
                'door1' : row[5],
                'door2' : row[6],
                }
        all_users.append(user) # each user gets added as a dict.

    conn.close()  # no commit() when just reading data
    return all_users

def changeDoorState(doorId, value):
    conn = sqlite3.connect('./static/myapp.db')
    curs = conn.cursor()
    curs.execute(f'UPDATE users SET {doorId} = ?', (value))
    # HERE HARDWARE CODE
    conn.commit()
    conn.close()

    return (f'DOOR : {doorId} STATE : {value} changed successfully!')



@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update():
    # Get form data
    email = request.form['id']
    is_admin = request.form.get('isAdmin')
    if is_admin is not None:
        is_admin = 1
    else: is_admin = 0
    door1 = request.form.get('door1')
    if door1 is not None:
        door1 = 1
    else: door1 = 0
    door2 = request.form.get('door2')
    if door2 is not None:
        door2 = 1
    else: door2 = 0
    print(email, is_admin, door1, door2)

    conn = sqlite3.connect('./static/myapp.db')
    curs = conn.cursor()
    curs.execute('UPDATE users SET _isAdmin=?, door1=?, door2=? WHERE email=?', (is_admin, door1, door2, email))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/admin')
def admin():
    if session['_isAdmin'] == 1:
        conn = sqlite3.connect('./static/myapp.db')
        curs = conn.cursor()
        curs.execute('SELECT * FROM users')
        users = curs.fetchall()
        return render_template('admin.html', users=users)
    else : return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    if 'email' in session:
        # Get user info from database using session['user_id']
        conn = sqlite3.connect('./static/myapp.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email = ?', (session['email'],))
        user = c.fetchone()
        conn.close()

        return render_template('profile.html', user=user)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get user input from form
        email = request.form['email']
        password = request.form['password']

        # Get user info from database
        conn = sqlite3.connect('./static/myapp.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = c.fetchone()
        conn.close()
        print("something")

        # Check if user exists and password is correct
        if user and password:
            # Store user info in session
            print(user)
            # name, email, password, phone
            session['email'] = user[1]
            session['name'] = user[0]
            session['_isAdmin'] = user[4]
            session['door1'] = user[5]
            session['door2'] = user[6]
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/allusers')
def allusers():
    return render_template("allusers.html", data= get_all_users())

@app.route('/signup', )
def signup():
   return render_template('signup.html') # redirect to a index to log in

@app.route('/post-user' , methods=['POST'])
def post_user():
    print("post_user noW!!")
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    pw = request.form['password']
    # CREATE TABLE users(name TEXT NOT NULL, email TEXT NOT NULL, phone TEXT, password TEXT NOT NULL, _isAdmin INTEGER DEFAULT 0 NOT NULL, door1 INTEGER DEFAULT 0 NOT NULL, door2 INTEGER DEFAULT 0 NOT NULL );
    # INSERT INTO users(name, email, phone, password, _isAdmin, door1, door2) VALUES ('Alex Riabov', 'aleksandr.riabov@csedge.org', '+12345678901', 'password', '1', '0', '0');
    store_user(name, email, phone, pw) # a separate function

    return render_template('login.html')

@app.route('/api')
def api():
    r = requests.get('https://api.thecatapi.com/v1/images/search?limit=10')
    r.status_code
    data = r.json()
    return render_template("api.html", data=data)

if __name__=="__main__":
    app.run(debug=True,host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 4444)))
