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
    
i=1
password=''
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
            i=i+1
        
        
print(password)