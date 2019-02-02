from flask import Flask, render_template
import datetime
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

@app.route("/")
def hello():

	# do actions w rpi here
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %H:%M")
	templateData = {
		'title' : 'HELLO!',
		'time': timeString
	}
	return render_template('main.html', **templateData)

@app.route("/readPin/<pin>")
def readPin(pin):
   try:
      GPIO.setup(int(pin), GPIO.IN)
      if GPIO.input(int(pin)) == True:
         response = "Pin number " + pin + " is high!"
      else:
         response = "Pin number " + pin + " is low!"
   except:
      response = "There was an error reading pin " + pin + "."

   templateData = {
      'title' : 'Status of Pin' + pin,
      'response' : response
      }

   return render_template('pin.html', **templateData)


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8000, debug=True)


# servoPIN = 17

# NUM_VITAMINS = 5

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(servoPIN, GPIO.OUT)

# p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
# p.start(2.5) # Initialization
# try:
# 	while True:
# 		p.ChangeDutyCycle(5)
# 		time.sleep(0.5)
# 		p.ChangeDutyCycle(7.5)
# 		time.sleep(0.5)
# 		p.ChangeDutyCycle(10)
# 		time.sleep(0.5)
# 		p.ChangeDutyCycle(12.5)
# 		time.sleep(0.5)
# 		p.ChangeDutyCycle(10)
# 		time.sleep(0.5)
# 		p.ChangeDutyCycle(7.5)
# 		time.sleep(0.5)
# 		p.ChangeDutyCycle(5)
# 		time.sleep(0.5)
# 		p.ChangeDutyCycle(2.5)
# 		time.sleep(0.5)
# except KeyboardInterrupt:
# 	p.stop()
# 	GPIO.cleanup()