from flask import Flask
from flask import request
from flask import render_template
from main import build_stories
from main import very_bad_code

import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/update_stories',methods=['GET','POST'])
def update_stories():
	file_name = json.loads(request.data).get('file_name')
	up_name = json.loads(request.data).get('upvoted')
	down_name = json.loads(request.data).get('downvoted')
	upvoted =  up_name.split(',')
	downvoted = down_name.split(',')
	story = very_bad_code(file_name,upvoted, downvoted)
	return json.dumps(story)

@app.route('/stories',methods=['GET','POST'])
def stories():
	file_name = json.loads(request.data).get('file_name')
	story = build_stories(file_name)
	return json.dumps(story)

if __name__ == '__main__':
	while True:
		try:
			app.run(host="127.0.0.1",use_reloader = False,debug=True, threaded=True)
		except:
			pass