from flask import Flask
from flask import request
from flask import render_template
from main import build_stories

import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/stories',methods=['GET','POST'])
def stories():
	print 'GOT IT'
	file_name = json.loads(request.data).get('file_name')
	story = build_stories(file_name)
	return json.dumps(story)


if __name__ == '__main__':
	app.run(host="127.0.0.1")