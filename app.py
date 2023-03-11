import sqlite3
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

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

def loginUser(email, pw):
    conn = sqlite3.connect('./static/myapp.db')
    curs = conn.cursor()
    print("Login")
    statement = f"SELECT name from users WHERE email='{email}' AND password = '{pw}';"
    curs.execute(statement)
    if not curs.fetchone():  # An empty result evaluates to False.
        print("Login failed")
        return False
    else:
        print("Welcome")
        return True

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/allusers')
def allusers():
    return render_template("allusers.html", data= get_all_users())

@app.route('/signup', )
def signup():
   return render_template('signup.html') # redirect to a index to log in

@app.route('/signin', )
def signin():
   return render_template('signin.html') 

@app.route('/login-user' , methods=['POST'])
def login_user():
    email = request.form['email']
    pw = request.form['password']
    print("Login")
    if loginUser(email,pw) == True :
        return render_template('index.html')
    else :
        return render_template('signin.html')

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
