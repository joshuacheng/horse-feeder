from flask import Flask, request, render_template
import requests
import string
import re
import json
import base64
import asyncio
import websockets

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from google.cloud import firestore
from gcloud import pubsub

import socket

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': 'horse-feeder',
})
db = firestore.Client()

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html') 

# add a new horse
@app.route('/handle_request')
def handleRequest():
	# horse data
	horse_code = request.args.get("code")
	print(horse_code)
	one = request.args.get("1")
	print(one)
	two = request.args.get("2")
	three = request.args.get("3")
	four = request.args.get("4")
	five = request.args.get("5")

	if not horse_code:
		return '''<html>
					<head>
						<title>Home Page - Microblog</title>
					</head>
					<body>
						<h1>please enter an id</h1>
					</body>
				</html>'''

	ref = db.collection(u'horses').document(horse_code)

	if request.args.get('new_horse'):
		ref.set({
			'vitamin_1': {
				'max': int(one),
				'taken': 0
			},
			'vitamin_2': {
				'max': int(two),
				'taken': 0
			},
			'vitamin_3': {
				'max': int(three),
				'taken': 0
			},
			'vitamin_4': {
				'max': int(four),
				'taken': 0
			},
			'vitamin_5':  {
				'max': int(five),
				'taken': 0
			}
		})
		msg = 'set stuff successfully'
	elif request.args.get('get_info'):
		msg = 'get info!'

		
	print(ref.get().to_dict())

	return render_template('submitted.html', msg = msg)

# GET / check_vitamin_dose : check if horse needs more vitamins for the day
@app.route('/check_vitamin_dose')
def check():
	vitamin_name = request.args.get("vitamin_name")
	horse_name = request.args.get("horse_code")

	users_ref = db.collection(u'horses').document(horse_name).collection(vitamin_name)
	try:
		doc = users_ref.get()
		print(doc)
	except google.cloud.exceptions.NotFound:
		print(u'No such document!')

	return 'yes'

# GET / action : execute action on RPi
@app.route('/action')
def action():
	dictToSend = {'horse':'horse01'}
	users_ref = db.collection(u'horses')

	docs = users_ref.get()

	for doc in docs:
		print(u'{} => {}'.format(doc.id, doc.to_dict()))

	res = requests.post('http://localhost:8000', json=dictToSend)
	print(res.text)
	dictFromServer = res.json()
	return "done"

# GET / horse : get all information about horse AND execute action on RPi
@app.route('/horse')
def horse():
	vitamin_name = request.args.get("horse")
	users_ref = db.collection(u'horses').document(vitamin_name)
	try:
		doc = users_ref.get()
		print(u'Document data: {}'.format(doc.to_dict()))
		dictToSend = format(doc.to_dict())
		res = requests.post('http://localhost:8000', json=dictToSend)
	except google.cloud.exceptions.NotFound:
		print(u'No such document!')

	return "fuckyea"

if __name__ == '__main__':
		app.run()
