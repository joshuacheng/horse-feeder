from flask import Flask, render_template,request, redirect, url_for, jsonify
import serial
import time
import json

app = Flask(__name__)

# initialize connection to Arduino
# if your arduino was running on a serial port other than '/dev/ttyACM0/'
# declare: a = Arduino(serial_port='/dev/ttyXXXX')
#a = Arduino("COM3") 
#time.sleep(3)
connected = False
ser = serial.Serial('COM7', 9600)
# declare the pins we're using
SWEEP_PIN = 9
# initial angle of the rotor - should go from 0 to 180 degrees relative to the initial
pos = 0

# initialize the digital pin as output
# a.set_pin_mode(SWEEP_PIN,'O')

# GET = we just type in the url
# POST = some sort of form submission like a button

@app.route('/', methods = ['POST','GET'])
def sweep_pyduino():
    ser.open()
    while not connected:
        serin = ser.read()
        connected = True
    # Post request to webpage - the user's selection of items returns sequence of what buckets to stop at
    #if request.method == 'POST':
    #    print("hey u fuk")
    #    print(jsonify(request.json))
    #    j = request.get_json()
        j={"vitamin_1":0, "vitamin_2":0, "vitamin_3":1, "vitamin_4":1, "vitamin_5":1}
        lst = []
        for i in range(1,6):
            num = int(j['vitamin_' + str(i)])
            lst.append(num)
        print(j)
        ser.write(str(bytearray(lst)))
    ser.close()
    return "lol"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
