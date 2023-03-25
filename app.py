import sqlite3
import requests
from flask import Flask, render_template, request, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'my_key'

def store_user(name, email, phone, pw):
    conn = sqlite3.connect('./static/myapp.db')
    curs = conn.cursor()
    curs.execute("INSERT INTO users (name, email, password, phone) VALUES((?),(?),(?),(?))",
        (name, email, pw, phone))

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
                }
        all_users.append(user) # each user gets added as a dict.

    conn.close()  # no commit() when just reading data
    return all_users

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    if 'user_id' in session:
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
    
    store_user(name, email, phone, pw) # a separate function

    return render_template('index.html')

@app.route('/api')
def api():
    r = requests.get('https://api.thecatapi.com/v1/images/search?limit=10')
    r.status_code
    data = r.json()
    return render_template("api.html", data=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
