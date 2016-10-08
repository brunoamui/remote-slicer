# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, render_template, request, url_for, jsonify
from executor import threadedSlicerExecutor
import urllib
import time
import redis
from rq import Queue
import server
import uuid
from flask_cors import CORS, cross_origin

# Initialize the Flask application
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

conn = redis.from_url("redis://redistogo:436473da6c8d57832bbf8ac3235490a0@sculpin.redistogo.com:10283")
q = Queue(connection=conn)

meshList = []


# Define a route for the default URL, which loads the form
@app.route('/')
def form():
    return render_template('form_submit.html')

# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is
# accepting: POST requests in this case
@app.route('/submit/', methods=['POST', 'OPTIONS'])
def submit():
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Max-Age': 1000,
            'Access-Control-Allow-Headers': 'origin, x-csrftoken, content-type, accept',
        }
        return '', 200, headers
    url=request.form['URL']
    result_aux = q.enqueue(server.processMeshUrl, url)
    uid = uuid.uuid1().hex
    meshList.append((uid, result_aux))
    return jsonify({"status": "OK",
                    "uid": uid}), 201

@app.route('/status/')
def status():
    result_aux = {tuple[0]:tuple[1].result for tuple in meshList}
    return jsonify(result_aux)


# Run the app :)
if __name__ == '__main__':
    app.debug = True
    app.run(
        host="0.0.0.0",
        port=int("80")
        )
