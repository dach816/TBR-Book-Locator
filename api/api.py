import time
import integrations
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/api/query/everand')
def get_everand_books(query):
    # TODO - handle exceptions
    return integrations.query_everand(query)

@app.route('/api/query/hardcover')
def search_hardcover(query):
    return integrations.search_hardcover(query, os.getenv('HARDCOVER_TOKEN'))