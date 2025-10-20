import time
import integrations
from flask import Flask, abort, jsonify, request
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route('/api/query/everand', methods=['POST'])
def get_everand_books():
    data = request.json
    if not data:
        abort(400, description="No data")

    isbns = data.get("isbns")
    if not isbns:
        abort(400, description="No ISBNs")
    
    try:
        return integrations.query_everand_isbns(isbns)
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

@app.errorhandler(400)
def handle_user_exception(error):
    response = jsonify({'message': error.description})
    return response, 400