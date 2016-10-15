# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, render_template, request, url_for, jsonify, g
from executor import threadedSlicerExecutor
import urllib
import time
import redis
from rq import Queue, Connection
import server
import uuid
from flask_cors import CORS, cross_origin
import dill as pickle
from server_config import cfg

# Initialize the Flask application
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# conn = redis.from_url("redis://redistogo:436473da6c8d57832bbf8ac3235490a0@sculpin.redistogo.com:10283")
rq_conn = redis.StrictRedis(host=cfg.redis["host"], port=cfg.redis["port"], password=cfg.redis["password"])

q = Queue(connection=rq_conn)



# Define a route for the default URL, which loads the form
@app.route('/')
def form():
    return render_template('form_submit.html')

# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is
# accepting: POST requests in this case
@app.route('/submit/', methods=['POST'])
def submit():
    url = request.form['URL']

    result_aux = q.enqueue(server.processMeshUrl, url)
    uid = uuid.uuid1().hex

    conn = redis.StrictRedis(host=cfg.redis["host"], port=cfg.redis["port"], password=cfg.redis["password"])
    meshList = pickle.loads(conn.get('meshList'))
    meshList.append((uid, result_aux))
    conn.set('meshList', pickle.dumps(meshList))

    return jsonify({"status": "OK",
                    "uid": uid})

@app.route('/status/')
def status():
    conn = redis.StrictRedis(host=cfg.redis["host"], port=cfg.redis["port"], password=cfg.redis["password"])
    meshList = pickle.loads(conn.get('meshList'))

    result_aux = {tuple[0]: tuple[1].result for tuple in meshList}
    return jsonify(result_aux)


# Run the app :)
if __name__ == '__main__':
    app.debug = True
    app.run(
        host="0.0.0.0",
        port=int("8080")
        )
