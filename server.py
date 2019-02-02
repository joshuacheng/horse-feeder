from flask import Flask, request, render_template
import urllib.request
import requests
import string
import re
import json
# from image_line import execute_zhang_suen
import base64

# firebase shit
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore
# cred = credentials.ApplicationDefault()
# firebase_admin.initialize_app(cred, {
#   'projectId': project_id,
# })

db = firestore.client()

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
    return "hehe xd"

if __name__ == '__main__':
        app.run()
