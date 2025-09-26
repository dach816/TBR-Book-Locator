import time
import integrations
from flask import Flask

app = Flask(__name__)

@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/api/query/everand')
def get_everand_books(query):
    # TODO - handle exceptions
    return integrations.query_everand(query)