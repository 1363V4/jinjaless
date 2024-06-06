from flask import Flask, request, Response
from components import home_page, result_container
import utils

app = Flask(__name__)

@app.route('/')
def index():
    context = None
    return Response(home_page(context))

@app.route('/search', methods=['POST'])
def search():
    input_value = request.form.get('searchbar')
    results = utils.get_results(input_value)
    return Response(result_container(results))

if __name__ == '__main__':
    app.run(debug=True)
