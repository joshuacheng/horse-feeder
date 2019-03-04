from flask import Flask, render_template,request, redirect, url_for
from pyduino import *
import time

app = Flask(__name__)

# initialize connection to Arduino
# if your arduino was running on a serial port other than '/dev/ttyACM0/'
# declare: a = Arduino(serial_port='/dev/ttyXXXX')
a = Arduino() 
time.sleep(3)

# declare the pins we're using
SWEEP_PIN = 9
# initial angle of the rotor - should go from 0 to 180 degrees relative to the initial
pos = 0

# initialize the digital pin as output
a.set_pin_mode(SWEEP_PIN,'O')

# GET = we just type in the url
# POST = some sort of form submission like a button
@app.route('/', methods = ['POST','GET'])

def sweep_pyduino():
    # Post request to webpage - the user's selection of items returns sequence of what buckets to stop at
    if request.method == 'POST':
        # if the bucket stops
        # TODO add delay values and change what form is checked
        # if request.form['submit'] == 'True': 
            # Stop at the bucket
        #    a.digital_write(LED_PIN,0)
        # if the bucket doesn't stop
        #elif request.form['submit'] == 'Turn Off': 
            # Keep going
        #    a.digital_write(SWEEP_PIN,30)
        #else:
        #    pass
        print(request.form)

if __name__ == "__main__":

    # lets launch our webpage!
    # do 0.0.0.0 so that we can log into this webpage
    # using another computer on the same network later
    app.run(host='http://127.0.0.1:5000/')