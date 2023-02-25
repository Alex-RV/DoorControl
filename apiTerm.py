import requests
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    r = requests.get('https://api.thecatapi.com/v1/images/search?limit=10')
    r.status_code
    data = r.json()
    return render_template("index.html", data=data)
 

if __name__ == '__main__':
    app.run()
