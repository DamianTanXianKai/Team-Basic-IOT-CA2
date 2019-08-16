#!/usr/bin/env python
# -*- coding: utf8 -*-
 
import sys
import Adafruit_DHT
import mysql.connector
import RPi.GPIO as GPIO
import MFRC522
import signal
import time
 
continue_reading = True
 
# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    continue_reading = False
    GPIO.cleanup()
 
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)
 
# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
 
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
 
    # If a card is found
    if status == MIFAREReader.MI_OK:
	time.sleep(2)   

    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
 
    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
 
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)
        
        #ENTER Your Card UID here
        my_uid = [136,4,94,213,7]
        
        #Configure LED Output Pin
        LED = 18
        GPIO.setup(LED, GPIO.OUT)
        GPIO.output(LED, GPIO.LOW)

        uid1 = ''.join(str(e) for e in uid)
        uid1.replace("'","")
        cnx = mysql.connector.connect(user='iotuser',password='dmitiot',host='localhost',database='iotdatabase')  
        cursor = cnx.cursor() 
        cursor.execute("Select rfid_values FROM rfid WHERE rfid_values =('%s')" %uid1)
        result = cursor.fetchone()

        
        #Check to see if card UID read matches your card UID
        if cursor.rowcount == 1:                #Open the Doggy Door if matching UIDs
            print("Access Granted - {}".format(uid1)),;
            GPIO.output(LED, GPIO.HIGH)  #Turn on LED
            time.sleep(5)                #Wait 5 Seconds
            GPIO.output(LED, GPIO.LOW)   #Turn off LED
            
        else:                            #Don't open if UIDs don't match
            print("Access Denied - {}".format(uid1)),;
        
##        # Authenticate
##        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
##
##        # Check if authenticated
##        if status == MIFAREReader.MI_OK:
##            MIFAREReader.MFRC522_Read(8)
##            MIFAREReader.MFRC522_StopCrypto1()
##        else:
##            print "Authentication error"

