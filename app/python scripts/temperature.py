import Adafruit_DHT
import time
import firebase_admin
from firebase_admin import credentials, firestore
import datetime
from gpiozero import CPUTemperature

cred = credentials.Certificate("/home/pi/Desktop/labo-3-firebase-nmdgent-jefverme/sensehat_dashboard/config/labo-iot-firebase-adminsdk-c3rpv-23eb19a6ee.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

sensor = Adafruit_DHT.DHT11
pin = 23

while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    cpuTemp = CPUTemperature()
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
        data = {
            u'temperature': temperature,
            u'humidity': humidity,
            u'date': datetime.datetime.now()
        }
        db.collection(u'sensoren').document(u'tempEnHumidity').set(data)
    else:
        print('Failed to get reading. Try again!')
        sys.exit(1)
    print(cpuTemp.temperature)
    db.collection(u'sensoren').document(u'cpuTemp').set({u'temp': cpuTemp.temperature})
    time.sleep(10)
