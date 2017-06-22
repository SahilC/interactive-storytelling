from flask import Flask
from flask import request
from main import build_stories

import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/stories')
def stories():
	file_name = request.args.get('file_name')
	story = build_stories(file_name)
	return json.dumps(story)


if __name__ == '__main__':
	app.run(host="127.0.0.1")