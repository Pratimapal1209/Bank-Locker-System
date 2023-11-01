import RPi_I2C_driver
import Recognize
import Recognize
mylcd = RPi_I2C_driver.lcd()
import time
mylcd.lcd_clear()
mylcd.lcd_display_string("Automatic bank", 1)
mylcd.lcd_display_string("Locker Ststem", 2)
time.sleep(0.5)

import serial
import RPi.GPIO as GPIO
import time

L1 = 5
L2 = 6
L3 = 13
L4 = 19

C1 = 12
C2 = 16
C3 = 20
C4 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    x=10
    if(GPIO.input(C1) == 1):
        x=characters[0]
    if(GPIO.input(C2) == 1):
        x=characters[1]
    if(GPIO.input(C3) == 1):
        x=characters[2]
    if(GPIO.input(C4) == 1):
        x=characters[3]
    GPIO.output(line, GPIO.LOW)
    return x

import adafruit_fingerprint




finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)
def get_fingerprint():
    """Get a finger print image, template it, and see if it matches!"""
    print("Waiting for image...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    print("Searching...")
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    return True



def get_fingerprint_detail():
    """Get a finger print image, template it, and see if it matches!
    This time, print out each error instead of just returning on failure"""
    print("Getting image...", end="", flush=True)
    i = finger.get_image()
    if i == adafruit_fingerprint.OK:
        print("Image taken")
    else:
        if i == adafruit_fingerprint.NOFINGER:
            print("No finger detected")
        elif i == adafruit_fingerprint.IMAGEFAIL:
            print("Imaging error")
        else:
            print("Other error")
        return False

    print("Templating...", end="", flush=True)
    i = finger.image_2_tz(1)
    if i == adafruit_fingerprint.OK:
        print("Templated")
    else:
        if i == adafruit_fingerprint.IMAGEMESS:
            print("Image too messy")
        elif i == adafruit_fingerprint.FEATUREFAIL:
            print("Could not identify features")
        elif i == adafruit_fingerprint.INVALIDIMAGE:
            print("Image invalid")
        else:
            print("Other error")
        return False

    print("Searching...", end="", flush=True)
    i = finger.finger_fast_search()
    
    if i == adafruit_fingerprint.OK:
        print("Found fingerprint!")
        return True
    else:
        if i == adafruit_fingerprint.NOTFOUND:
            print("No match found")
        else:
            print("Other error")
        return False


# pylint: disable=too-many-statements
def enroll_finger(location):
    """Take a 2 finger images and template it, then store in 'location'"""
    for fingerimg in range(1, 3):
        if fingerimg == 1:
            print("Place finger on sensor...", end="", flush=True)
        else:
            print("Place same finger again...", end="", flush=True)

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="", flush=True)
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                return False
            else:
                print("Other error")
                return False

        print("Templating...", end="", flush=True)
        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            print("Templated")
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                print("Image too messy")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                print("Could not identify features")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                print("Image invalid")
            else:
                print("Other error")
            return False

        if fingerimg == 1:
            print("Remove finger")
            time.sleep(1)
            while i != adafruit_fingerprint.NOFINGER:
                i = finger.get_image()

    print("Creating model...", end="", flush=True)
    i = finger.create_model()
    if i == adafruit_fingerprint.OK:
        print("Created")
    else:
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            print("Prints did not match")
        else:
            print("Other error")
        return False

    print("Storing model #%d..." % location, end="", flush=True)
    i = finger.store_model(location)
    if i == adafruit_fingerprint.OK:
        print("Stored")
    else:
        if i == adafruit_fingerprint.BADLOCATION:
            print("Bad storage location")
        elif i == adafruit_fingerprint.FLASHERR:
            print("Flash storage error")
        else:
            print("Other error")
        return False

    return True


def save_fingerprint_image(filename):
    """Scan fingerprint then save image to filename."""
    print("Place finger on sensor...", end="", flush=True)
    while True:
        i = finger.get_image()
        if i == adafruit_fingerprint.OK:
            print("Image taken")
            break
        if i == adafruit_fingerprint.NOFINGER:
            print(".", end="", flush=True)
        elif i == adafruit_fingerprint.IMAGEFAIL:
            print("Imaging error")
            return False
        else:
            print("Other error")
            return False

    from PIL import Image  

    img = Image.new("L", (192, 192), "white")
    pixeldata = img.load()
    mask = 0b00001111
    result = finger.get_fpdata(sensorbuffer="image")

 
    x = 0
    
    y = 0
 
    for i in range(len(result)):
        pixeldata[x, y] = (int(result[i]) >> 4) * 17
        x += 1
        pixeldata[x, y] = (int(result[i]) & mask) * 17
        if x == 191:
            x = 0
            y += 1
        else:
            x += 1

    if not img.save(filename):
        return True
    return False





def get_num(max_number):
    """Use input() to get a valid number from 0 to the maximum size
    of the library. Retry till success!"""
    i = -1
    while (i > max_number - 1) or (i < 0):
        try:
            i = int(input("Enter ID # from 0-{}: ".format(max_number - 1)))
        except ValueError:
            pass
    return i


# initialize LED color
led_color = 1
led_mode = 3
ir=4
buzzer=23
lock=17
GPIO.setup(ir,GPIO.IN)
GPIO.setup(buzzer,GPIO.OUT)

GPIO.output(buzzer,False)
GPIO.setup(lock,GPIO.OUT)

GPIO.output(lock,True)
while True:
    finger.set_led(color=led_color, mode=led_mode)
    print("----------------")
    if finger.read_templates() != adafruit_fingerprint.OK:
        raise RuntimeError("Failed to read templates")
    print("Fingerprint templates: ", finger.templates)
    if finger.count_templates() != adafruit_fingerprint.OK:
        raise RuntimeError("Failed to read templates")
    print("Number of templates found: ", finger.template_count)
    if finger.read_sysparam() != adafruit_fingerprint.OK:
        raise RuntimeError("Failed to get system parameters")
    mylcd.lcd_clear()
    mylcd.lcd_display_string("Waiting for....", 1)
    mylcd.lcd_display_string("Oject detect....", 2)
    time.sleep(0.5)
    if GPIO.input(ir)==0:
        mylcd.lcd_clear()
        mylcd.lcd_display_string("Object detected....", 1)
        mylcd.lcd_display_string("place finerprint....", 2)
        time.sleep(1)
        GPIO.output(buzzer,True)
        time.sleep(1)
        GPIO.output(buzzer,False)
        finger.set_led(color=3, mode=1)
        
        if get_fingerprint():
            print("Detected #", finger.finger_id, "with confidence", finger.confidence)
        else:
            print("Finger not found")
        fid=finger.finger_id
        print('predicted person gesture id='+str([fid]))
    
        conf=finger.confidence
        print(conf)
        if (conf>50):
            mylcd.lcd_clear()
            mylcd.lcd_display_string("Finger print....", 1)
            mylcd.lcd_display_string("Matched....", 2)
            time.sleep(1)
            GPIO.output(buzzer,True)
            time.sleep(1)
            GPIO.output(buzzer,False)
            import random
            skey=''
            for i in range(4):
                skey=skey+str(random.randint(0,9))
            mylcd.lcd_clear()
            mylcd.lcd_display_string("Enter password....", 1)
            i=1
            password=''
            star=''
            print('enter password')
            while i<=5:
                a=readLine(L1, ["1","2","3","A"])
                b=readLine(L2, ["4","5","6","B"])
                c=readLine(L3, ["7","8","9","C"])
                d=readLine(L4, ["*","0","#","D"])
                time.sleep(0.2)
                if a!=10 or b!=10 or c!=10 or d!=10:
                    if a!=10:
                        key=a
                    if b!=10:
                        key=b
                    if c!=10:
                        key=c
                    if d!=10:
                        key=d
                    print(key)
                    password=password+str(key)
                    star=star+'*'
                    i=i+1
                    mylcd.lcd_display_string(star, 2)
            if password=='12345':
                time.sleep(1)
                mylcd.lcd_clear()
                mylcd.lcd_display_string("password....", 1)
                mylcd.lcd_display_string("Matched....", 2)
                time.sleep(1)
                GPIO.output(buzzer,True)
                time.sleep(1)
                GPIO.output(buzzer,False)
                SERIAL_PORT = "/dev/ttyAMA0"    # Raspberry Pi 3
                ser = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 5)

                ser.write("AT+CMGF=1\r".encode()) # set to text mode
                time.sleep(1)
                ser.write('AT+CMGDA="DEL ALL"\r'.encode()) # delete all SMS
                time.sleep(1)
                print( "Listening for incomming SMS...")
                ser.write('AT+CMGS="+919611895624"\r'.encode())
                time.sleep(1)
                msg = "bank locker otp="+skey
                ser.write(msg.encode() + chr(26).encode())
                time.sleep(1)
                ser.write('AT+CMGDA="DEL ALL"\r'.encode()) # delete all
                mylcd.lcd_clear()
                mylcd.lcd_display_string("Enter OTP....", 1)
                print(skey)
                time.sleep(1)
                i=1
                password=''
                star=''
                print('enter OTP')
                while i<=4:
                    a=readLine(L1, ["1","2","3","A"])
                    b=readLine(L2, ["4","5","6","B"])
                    c=readLine(L3, ["7","8","9","C"])
                    d=readLine(L4, ["*","0","#","D"])
                    time.sleep(0.2)
                    if a!=10 or b!=10 or c!=10 or d!=10:
                        if a!=10:
                            key=a
                        if b!=10:
                            key=b
                        if c!=10:
                            key=c
                        if d!=10:
                            key=d
                        print(key)
                        password=password+str(key)
                        star=star+'*'
                        i=i+1
                        mylcd.lcd_display_string(star, 2)
                if password==skey:
                    time.sleep(1)
                    mylcd.lcd_clear()
                    mylcd.lcd_display_string("OTP ....", 1)
                    mylcd.lcd_display_string("Matched....", 2)
                    time.sleep(1)
                    time.sleep(1)
                    GPIO.output(buzzer,True)
                    time.sleep(1)
                    GPIO.output(buzzer,False)
                    mylcd.lcd_clear()
                    mylcd.lcd_display_string("Face capturing....", 1)   
                    Id=Recognize.recognize_face()
                    print(Id)
                    time.sleep(1)
                    if Id[0]=='pratibha' or Id[0]=='pratibha':
                        time.sleep(1)
                        mylcd.lcd_clear()
                        mylcd.lcd_display_string("Face....", 1)
                        mylcd.lcd_display_string("Matched....", 2)
                        time.sleep(1)
                        GPIO.output(buzzer,True)
                        time.sleep(1)
                        GPIO.output(buzzer,False)
                        time.sleep(1)
                        mylcd.lcd_clear()
                        mylcd.lcd_display_string("Bank locker....", 1)
                        mylcd.lcd_display_string("Openned....", 2)
                        time.sleep(1)
                        GPIO.output(lock,False)
                        time.sleep(4)
                        GPIO.output(lock,True)
                        break
                    else:
                        mylcd.lcd_clear()
                        mylcd.lcd_display_string("Face....", 1)
                        mylcd.lcd_display_string("Not Matched....", 2)
                        time.sleep(1)
                        GPIO.output(buzzer,True)
                        time.sleep(5)
                        GPIO.output(buzzer,False)
                        SERIAL_PORT = "/dev/ttyAMA0"    # Raspberry Pi 3
                        ser = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 5)

                        ser.write("AT+CMGF=1\r".encode()) # set to text mode
                        time.sleep(1)
                        ser.write('AT+CMGDA="DEL ALL"\r'.encode()) # delete all SMS
                        time.sleep(1)
                        print( "Listening for incomming SMS...")
                        ser.write('AT+CMGS="+919611895624"\r'.encode())
                        time.sleep(1)
                        msg = "Some on trying to access your locker"
                        ser.write(msg.encode() + chr(26).encode())
                        time.sleep(1)
                        ser.write('AT+CMGDA="DEL ALL"\r'.encode()) # delete all
                        break
                else:
                    mylcd.lcd_clear()
                    mylcd.lcd_display_string("OTP....", 1)
                    mylcd.lcd_display_string("Not Matched....", 2)
                    time.sleep(1)
                    GPIO.output(buzzer,True)
                    time.sleep(5)
                    GPIO.output(buzzer,False)
                    SERIAL_PORT = "/dev/ttyAMA0"    # Raspberry Pi 3
                    ser = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 5)

                    ser.write("AT+CMGF=1\r".encode()) # set to text mode
                    time.sleep(1)
                    ser.write('AT+CMGDA="DEL ALL"\r'.encode()) # delete all SMS
                    time.sleep(1)
                    print( "Listening for incomming SMS...")
                    ser.write('AT+CMGS="+919611895624"\r'.encode())
                    time.sleep(1)
                    msg = "Some on trying to access your locker"
                    ser.write(msg.encode() + chr(26).encode())
                    time.sleep(1)
                    ser.write('AT+CMGDA="DEL ALL"\r'.encode()) # delete all
                    break
            else:
                mylcd.lcd_clear()
                mylcd.lcd_display_string("password....", 1)
                mylcd.lcd_display_string("Not Matched....", 2)
                time.sleep(1)
                GPIO.output(buzzer,True)
                time.sleep(5)
                GPIO.output(buzzer,False)
                SERIAL_PORT = "/dev/ttyAMA0"    # Raspberry Pi 3
                ser = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 5)

                ser.write("AT+CMGF=1\r".encode()) # set to text mode
                time.sleep(1)
                ser.write('AT+CMGDA="DEL ALL"\r'.encode()) # delete all SMS
                time.sleep(1)
                print( "Listening for incomming SMS...")
                ser.write('AT+CMGS="+919611895624"\r'.encode())
                time.sleep(1)
                msg = "Some on trying to access your locker"
                ser.write(msg.encode() + chr(26).encode())
                time.sleep(1)
                ser.write('AT+CMGDA="DEL ALL"\r'.encode()) # delete all
                break
            
                
        else:
            mylcd.lcd_clear()
            mylcd.lcd_display_string("Finger print....", 1)
            mylcd.lcd_display_string("Not Matched....", 2)
            time.sleep(1)
            GPIO.output(buzzer,True)
            time.sleep(5)
            GPIO.output(buzzer,False)
            print('Finger print not matching')
            SERIAL_PORT = "/dev/ttyAMA0"    # Raspberry Pi 3
            ser = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 5)

            ser.write("AT+CMGF=1\r".encode()) # set to text mode
            time.sleep(1)
            ser.write('AT+CMGDA="DEL ALL"\r'.encode()) # delete all SMS
            time.sleep(1)
            print( "Listening for incomming SMS...")
            ser.write('AT+CMGS="+917349595293"\r'.encode())
            time.sleep(1)
            msg = "Some on trying to access your locker"
            ser.write(msg.encode() + chr(26).encode())
            time.sleep(1)
            ser.write('AT+CMGDA="DEL ALL"\r'.encode()) # delete all
            break
            
mylcd.lcd_clear()
mylcd.lcd_display_string("Bank locker system", 1)
mylcd.lcd_display_string("Run again", 2)
time.sleep(1)       