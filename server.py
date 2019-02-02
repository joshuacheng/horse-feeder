from flask import Flask, request, render_template
# import urllib.request
import requests
import string
import re
import json
# from image_line import execute_zhang_suen
import base64

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from google.cloud import firestore
from gcloud import pubsub

# import 'firebase/firestore'

# Fetch the service account key JSON file contents
#cred = credentials.Certificate('horse-feeder-2175ba8ce0c1.json')
# Initialize the app with a service account, granting admin privileges
#firebase_admin.initialize_app(cred, {
#	'databaseURL': 'https://horse-feeder.firebaseio.com/'
#z})

db = firestore.Client()
client = pubsub.Client('horse-feeder')
app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html') 

# add a new horse
@app.route('/new_horse')
def new_horse():
	# horse data
	horse_code = request.args.get("code")
	one = request.args.get("1")
	two = request.args.get("2")
	three = request.args.get("3")
	four = request.args.get("4")
	five = request.args.get("5")

	ref = db.collection(u'horses').document(horse_code)
	ref.set({
		'vitamin_1': {
			'max': one,
			'taken': 0
		},
		'vitamin_2': {
			'max': one,
			'taken': 0
		},
		'vitamin_3': {
			'max': one,
			'taken': 0
		},
		'vitamin_4': {
			'max': one,
			'taken': 0
		},
		'vitamin_5':  {
			'max': one,
			'taken': 0
		}
	})

    # print(request.args)
    return render_template('submitted.html')

# should this horse be fed the vitamin
@app.route('/check_vitamin_dose')
def check():
	vitamin_name = request.args.get("vitamin_name")
	return True

if __name__ == '__main__':
		app.run()
