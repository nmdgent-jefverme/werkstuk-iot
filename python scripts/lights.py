#! /usr/bin/python3
from gpiozero import LED
import firebase_admin
from firebase_admin import credentials, firestore
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)

cred = credentials.Certificate("/home/pi/Desktop/labo-3-firebase-nmdgent-jefverme/sensehat_dashboard/config/labo-iot-firebase-adminsdk-c3rpv-23eb19a6ee.json")
firebase_admin.initialize_app(cred)

# Deze functie loopt over alle documenten in de collectie en 
# verandert de pinout state op basis van het 'active' veld
def update_lights(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        doc_readable = doc.to_dict()
        if doc_readable['naam'] == 'switch_1':
            if doc_readable['active']:
                GPIO.output(24, True)
            else:
                GPIO.output(24, False)
        elif doc_readable['naam'] == 'switch_2':
            if doc_readable['active']:
                GPIO.output(25, True)
            else:
                GPIO.output(25, False)
        elif doc_readable['naam'] == 'switch_3':
            if doc_readable['active']:
                GPIO.output(8, True)
            else:
                GPIO.output(8, False)
        elif doc_readable['naam'] == 'switch_4':
            if doc_readable['active']:
                GPIO.output(7, True)
            else:
                GPIO.output(7, False)

db = firestore.client()
pi_ref = db.collection('lights')
# event listener voor de collectie 'lights'
pi_watch = pi_ref.on_snapshot(update_lights)

while True:
    pass