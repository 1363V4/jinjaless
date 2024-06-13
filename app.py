from flask import Flask, redirect, request, Response, session, url_for
from components import home_page, input_swap, result_container, max_requests, snitch_page
from markupsafe import Markup
from dotenv import load_dotenv
import os
import utils


load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

@app.route('/')
def index():
    state = utils.get_topics()
    return Response(home_page(state))

@app.route('/search', methods=['POST'])
def search():    
    session['access_count'] = session.get('access_count', 0)
    session['access_count'] += 1
    if session['access_count'] > 5:
        return Response(max_requests())

    input_value = request.form.get('searchbar').lower()
    results = utils.get_results(input_value)
    
    return Response(result_container(results))

@app.route('/topic', methods=['POST'])
def topic():
    topic = request.form.get('topic')
    results = utils.get_results(topic)
    swap = input_swap(topic)
    return Response(Markup(swap) + str(result_container(results)))

@app.route('/reset', methods=['GET'])
def reset():
    utils.clean_db()
    return redirect(url_for('index'))

@app.route('/snitch', methods=['GET'])
def snitch():
    data = utils.get_searches()
    return Response(snitch_page(data))

if __name__ == '__main__':
    app.run(debug=True)
