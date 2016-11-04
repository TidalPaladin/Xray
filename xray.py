import transmit as RPT
import wiringpi as wpi
from subprocess import call
import subprocess

# Used to hide call output
import os
FNULL = open(os.devnull, 'w')

# Define transmit constants for Etekcity wireless wall outlets
ch1_on = "0001010001010101001100110"
ch1_off = "0001010001010101001111000"
ch2_on = "0001010001010101001111000"
ch2_off = "0001010001010101110011000"
pin = 0
high = 505
low = 120
period_t = 755

# Define camera settings for exposure
iso = 3200
shutter = 3


def beamon() :
    RPT.transmit(ch2_on, pin, 10, high, low, period_t)

def beamoff() :
    RPT.transmit(ch2_off, pin, 30, high, low, period_t)

def lighton() :
    RPT.transmit(ch2_on, pin, 15, high, low, period_t)

def lightoff() :
    RPT.transmit(ch1_off, pin, 30, high, low, period_t)

def setupCamera() :
    call(['gphoto2','--set-config',"iso="+str(iso), "shutterspeed2="+str(shutter)])

def testConnection() :
    retcode = call(['gphoto2','--summary'], stdout=FNULL, stderr=subprocess.STDOUT)
    return retcode

def captureImage(filename) :
    subprocess.Popen(['gphoto2','--force-overwrite','--keep','--capture-image-and-download','--filename=xray-'+filename+'.nef'], stdout=FNULL, stderr=subprocess.STDOUT)    

def main() :
    setupCamera
    print("Camera settings are {0} ISO, {1} seconds".format(iso, shutter))
    filename = input('Enter filename: ')
    print("Beginning capture in 3 seconds...")
    wpi.delay(3000)
    lightoff()
    captureImage(filename)
    beamon()
    wpi.delay(round((shutter-0.5)*1000))    #Delay some time before shutting off beam
    beamoff()

    wpi.delay(2000)
    lighton()
    return

if not testConnection() == 0 :
    print("Error communicating with camera")
else:
    main()
