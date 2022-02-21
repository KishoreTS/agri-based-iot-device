import RPi.GPIO as GPIO
from flask import Flask, render_template, request
app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#define sensors GPIOs
RFID = 20
IRsensor = 16
#define actuators GPIOs
motor = 13
audio = 19
led = 26
#initialize GPIO status variables
RFIDSts = 0
IRsensorSts = 0
motorSts = 0
audioSts = 0
ledSts = 0
# Define button and PIR sensor pins as an input
GPIO.setup(RFID, GPIO.IN)   
GPIO.setup(IRsensor, GPIO.IN)
# Define led pins as output
GPIO.setup(motor, GPIO.OUT)   
GPIO.setup(audio, GPIO.OUT) 
GPIO.setup(led, GPIO.OUT) 
# turn leds OFF 
GPIO.output(motor, GPIO.LOW)
GPIO.output(audio, GPIO.LOW)
GPIO.output(led, GPIO.LOW)
	
@app.route("/")
def index():
	# Read GPIO Status
	RFIDSts = GPIO.input(RFID)
	IRsensorSts = GPIO.input(IRsensor)
	motorSts = GPIO.input(motor)
	audioSts = GPIO.input(audio)
	ledSts = GPIO.input(led)
	templateData = {
      		'RFID'  : RFIDSts,
      		'IRsensor'  : IRsensorSts,
      		'motor'  : motorSts,
      		'audio'  : audioSts,
      		'led'  : ledSts,
      	}
	return render_template('index.html', **templateData)
	
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
	if deviceName == 'motor':
		actuator = motor
	if deviceName == 'audio':
		actuator = audio
	if deviceName == 'led':
		actuator = led
   
	if action == "on":
		GPIO.output(actuator, GPIO.HIGH)
	if action == "off":
		GPIO.output(actuator, GPIO.LOW)
		     
	RFIDSts = GPIO.input(RFID)
	IRsensorSts = GPIO.input(IRsensor)
	motorSts = GPIO.input(motor)
	audioSts = GPIO.input(audio)
	ledSts = GPIO.input(led)
   
	templateData = {
	 	'RFID'  : RFIDSts,
      		'IRsensor'  : IRsensorSts,
      		'motor'  : motorSts,
      		'audio'  : audioSts,
      		'led'  : ledSts,
	}
	return render_template('index.html', **templateData)
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
