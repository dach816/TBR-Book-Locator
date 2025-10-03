import time
import integrations
from flask import Flask, abort, jsonify, request
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/api/query/everand')
def get_everand_books(query):
    if not query:
        return

    try:
        return integrations.query_everand(query)
    except Exception as e:
        abort(500, description=e)

@app.route('/api/query/hardcover')
def search_hardcover():
    query = request.args.get('query')
    if not query:
        return

    try:
        return integrations.search_hardcover(query, os.getenv('HARDCOVER_TOKEN'))
    except Exception as e:
        abort(500, description=e)

@app.errorhandler(500)
def handle_generic_exception(error):
    response = jsonify({'message': error.description})
    return response, 500