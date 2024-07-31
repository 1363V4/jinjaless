from flask import Flask, redirect, request, Response, session, url_for
from components import home_page, input_swap, result_container, max_requests, snitch_page
from markupsafe import Markup
from dotenv import load_dotenv
import os
import utils
import redis

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
redis_client = redis.from_url("redis://red-cqku2c3qf0us73bprfa0:6379")

@app.route('/')
def index():
    state = utils.get_topics()
    return Response(home_page(state))

@app.route('/search', methods=['POST'])
def search():
    user_ip = request.remote_addr
    access_count = redis_client.get(user_ip)
    if access_count is None:
        redis_client.set(user_ip, 1, ex=3600)  # Set key with 1 hour expiration
    else:
        access_count = int(access_count)
        if access_count >= 5:
            return Response(max_requests())
        redis_client.incr(user_ip)

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
    utils.clean_db(redis_client)
    return redirect(url_for('index'))

@app.route('/snitch', methods=['GET'])
def snitch():
    data = utils.get_searches()
    return Response(snitch_page(data))

@app.route('/snatch', methods=['GET'])
def snatch():
    user_ips = redis_client.keys('*')
    return Response(snitch_page(user_ips))

if __name__ == '__main__':
    app.run()