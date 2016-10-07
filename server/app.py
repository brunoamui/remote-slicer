# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, render_template, request, url_for
from executor import threadedSlicerExecutor
import urllib
import time
import redis
from rq import Queue
import server


# Initialize the Flask application
app = Flask(__name__)

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
@app.route('/submit/', methods=['POST'])
def submit():
    url=request.form['URL']
    result_aux = q.enqueue(server.processMeshUrl, url)
    meshList.append((url, result_aux))
    return render_template('form_action.html', result="Adicionado")

@app.route('/status/')
def status():
    result_aux = []
    for tuple in meshList:
        result_aux.append((tuple[0], str(tuple[1].result)))
    return render_template('form_action.html', result=result_aux)


# Run the app :)
if __name__ == '__main__':
    app.debug = True
    app.run(
        host="0.0.0.0",
        port=int("8080")
        )
