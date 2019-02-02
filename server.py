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
		'vitamin_1': one,
		'vitamin_2': two, 
		'vitamin_3': three, 
		'vitamin_4': four, 
		'vitamin_5': five
	})

    # print(request.args)
    return render_template('submitted.html')

if __name__ == '__main__':
		app.run()
