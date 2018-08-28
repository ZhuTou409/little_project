import cv2
import RPi.GPIO as GPIO  
import time  
import signal  
import atexit

atexit.register(GPIO.cleanup)    
  
servopin = 12
servo_y = 20
GPIO.setmode(GPIO.BCM)  
GPIO.setup(servopin, GPIO.OUT, initial=False)
GPIO.setup(servo_y, GPIO.OUT, initial=False) 
p = GPIO.PWM(servopin,50) #50HZ
Y = GPIO.PWM(servo_y,50) #50HZ
p.start(0)
Y.start(0)
time.sleep(2)

cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 240)
face_cascade = cv2.CascadeClassifier( '/home/pi/opencv-3.4.1/data/lbpcascades/lbpcascade_frontalface.xml' ) 
x=0;
thisError_x=0
lastError_x=0
thisError_y=0
lastError_y=0
pwm_y=0
pwm = 7
Y_P = 7

while True:
    
    ret,frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale( gray )
    max_face = 0
    value_x = 0
    if len(faces)>0:
        #print('face found!')
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+h,y+w),(0,255,0),2)
            #max_face=w*h
            result = (x,y,w,h)
            x=result[0]
            y = result[1]
            #print (x)
        thisError_x=x-160
        thisError_y=y-120
        pwm_x = thisError_x*0.001+0.001*(thisError_x-lastError_x)
        pwm_y = thisError_y*0.001+0.001*(thisError_y-lastError_y)
        lastError_x = thisError_x
        lastError_y = thisError_y
        pwm+= pwm_x
        Y_P+= pwm_y
        if pwm>12:
            pwm=11
        if pwm<2.5:
            pwm=2.5
        if Y_P>12:
            Y_P=11
        if Y_P<2.5:
            Y_P=2.5
            
        print(pwm);
    p.ChangeDutyCycle(12.5-pwm)
    Y.ChangeDutyCycle(Y_P)
    time.sleep(0.02)
    p.ChangeDutyCycle(0)
    Y.ChangeDutyCycle(0)
    cv2.imshow("capture", frame)
    if cv2.waitKey(1)==119:
        break
cap.release()
cv2.destroyAllWindows()
    
