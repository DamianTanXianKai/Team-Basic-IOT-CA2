import sys
import Adafruit_DHT
import mysql.connector
import RPi.GPIO as GPIO
import MFRC522
import signal

uid = None
prev_uid = None 
continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
mfrc522 = MFRC522.MFRC522()


try:
    u='iotuser';pw='dmitiot';
    h='localhost';db='iotdatabase'

    cnx = mysql.connector.connect(user=u,password=pw,host=h,database=db) 
    cursor = cnx.cursor()
    # Scan for cards    
    (status,TagType) = mfrc522.MFRC522_Request(mfrc522.PICC_REQIDL)

    # If a card is found
    if status == mfrc522.MI_OK:
        # Get the UID of the card
        (status,uid) = mfrc522.MFRC522_Anticoll()
        if uid!=prev_uid:
           prev_uid = uid
           print("Card deleted! UID of card is {}".format(uid))
	   uid1 = ''.join(str(e) for e in uid)
           uid1.replace("'","")
	   print("{}".format(uid1))
           cursor.execute("INSERT INTO rfid (rfid_values) VALUES ('%s')" %(uid1))
           cnx.commit()
 
except:
    print(sys.exc_info()[0])
    print(sys.exc_info()[1])
