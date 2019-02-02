from flask import Flask, request, render_template

# from quart import Quart, websocket
# import urllib.request
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

# db = firestore.Client()
# client = pubsub.Client('horse-feeder')
app = Flask(__name__)

# async def abar(a):
# 	async with websockets.connect('ws://localhost:8765') as websocket:
# 		await websocket.send('horse01')

# loop = asyncio.get_event_loop()

@app.route('/')
def home():
	return render_template('index.html') 

# add a new horse
@app.route('/new_horse')
def new_horse():
	# horse data
	horse_code = request.args.get("code")
	one = request.form.get("1")
	two = request.form.get("2")
	three = request.form.get("3")
	four = request.form.get("4")
	five = request.form.get("5")

	ref = db.collection(u'horses').document(horse_code)
	ref.set({
		'vitamin_1': {
			'max': one,
			'taken': 0
		},
		'vitamin_2': {
			'max': two,
			'taken': 0
		},
		'vitamin_3': {
			'max': three,
			'taken': 0
		},
		'vitamin_4': {
			'max': four,
			'taken': 0
		},
		'vitamin_5':  {
			'max': five,
			'taken': 0
		}
	})
	return render_template('submitted.html')

# should this horse be fed the vitamin
@app.route('/check_vitamin_dose')
def check():
	vitamin_name = request.args.get("vitamin_name")
	return True

@app.route('/action')
def action():
	dictToSend = {'horse':'horse01'}
	res = requests.post('http://localhost:8000', json=dictToSend)
	print(res.text)
	dictFromServer = res.json()
	return "done"

if __name__ == '__main__':
		app.run()
