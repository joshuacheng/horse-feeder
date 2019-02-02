from flask import Flask, request, render_template

import requests
import string
import re
import json
import base64

app = Flask(__name__)

@app.route('/')
def home():
	return "lmao"

if __name__ == '__main__':
		app.run(host='0.0.0.0', port=8000)
