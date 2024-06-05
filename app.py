from flask import Flask, Response
from components import home_page

app = Flask(__name__)

@app.route('/')
def hello_world():
    return Response(home_page())

if __name__ == '__main__':
    app.run()
