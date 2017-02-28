#========
#AutoDrive Pi Car
#Harry
#2016.7.20
#========


import RPi.GPIO as GPIO
import time

a_1 = 11
a_2 = 12
b_1 = 15
b_2 = 16
servo_pin = 13
trig_pin = 31
echo_pin = 32

def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(a_1,GPIO.OUT,initial = False)
        GPIO.setup(a_2,GPIO.OUT,initial = False)
        GPIO.setup(b_1,GPIO.OUT,initial = False)
        GPIO.setup(b_2,GPIO.OUT,initial = False)
        GPIO.setup(servo_pin,GPIO.OUT,initial = False)
        GPIO.setup(trig_pin,GPIO.OUT,initial = False)
        GPIO.setup(echo_pin,GPIO.IN)
	return GPIO.PWM(servo_pin, 50)

def t_stop():
        GPIO.output(a_1, False)
        GPIO.output(a_2, False)
        GPIO.output(b_1, False)
        GPIO.output(b_2, False)

def t_up():
        GPIO.output(a_1, True)
        GPIO.output(a_2, False)
        GPIO.output(b_1, True)
        GPIO.output(b_2, False)

def t_down():
        GPIO.output(a_1, False)
        GPIO.output(a_2, True)
        GPIO.output(b_1, False)
        GPIO.output(b_2, True)

def t_left():
        GPIO.output(b_1, False)
        GPIO.output(b_2, True)
        GPIO.output(a_1, True)
        GPIO.output(a_2, False)

def t_right():
        GPIO.output(b_1, True)
        GPIO.output(b_2, False)
        GPIO.output(a_1, False)
        GPIO.output(a_2, True)

#0-stop,1-forward,2-backward,3-left,4-right
def action(order, duration):
	if order == 1:
		t_up()
	elif order == 2:
		t_down()
	elif order == 3:
		t_left()
	elif order == 4:
		t_right()
	time.sleep(duration)
	t_stop()

def servo_rot(servopwm,angle):
        servopwm.ChangeDutyCycle(2.5 + 10 * angle / 180)
        time.sleep(0.5)

def checkdist():
        GPIO.output(trig_pin,GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(trig_pin,GPIO.LOW)
        while not GPIO.input(echo_pin):
                pass
        t1 = time.time()
        while GPIO.input(echo_pin):
                pass
        t2 = time.time()
        return (t2-t1)*340/2

#return a direction with no barrier, 1-left, 2-right, 0-none
def detection(servopwm):
	servo_rot(servopwm, 20)
	rightdist = checkdist()
	servo_rot(servopwm, 170)
	leftdist = checkdist()
	servo_rot(servopwm, 90)
	print("left, right:")
	print(leftdist)
	print(rightdist)
	if leftdist >= 0.3 or rightdist >= 0.3:
		if leftdist <= rightdist:
			return 2
		elif leftdist > rightdist:
			return 1
	else:
		return 0

def turnleft():
	print("turnleft...")
	action(3,1)

def turnright():
	print("turnright...")
	action(4,1)

def turnback():
	print("turnback...")
	action(3,2.2)


###################################################
servo_pwm = setup()
servo_pwm.start(0)

#servo_rot(servo_pwm,10)
#servo_rot(servo_pwm,180)
#servo_rot(servo_pwm,90)
#print(detection(servo_pwm))

servo_rot(servo_pwm,90)
counter = 0
stop_counter = 0
lastdist = 0

try:
	while True:
		frontdist = checkdist()
		if abs(frontdist - lastdist) <= 0.005 or abs(frontdist - lastdist) >= 35:
			stop_counter = stop_counter + 1
		else:
			stop_counter = 0 
		print(frontdist)
		if frontdist <= 0.35:
			if counter > 3:
				counter = 0
				t_stop()
				rst = detection(servo_pwm)
				if rst == 1:
					turnleft()
				elif rst == 2:
					turnright()
				else:
					turnback()
			else:
				counter = counter + 1
		else:
			counter = 0
			t_up()
		if stop_counter > 10:
			print("stucked, going back...")
			stop_counter = 0
			t_stop()
			action(2,0.5)
			rst = detection(servo_pwm)
                	if rst == 1:
                		turnleft()
                        elif rst == 2:
        	                turnright()
                        else:
                                turnback()
		lastdist = frontdist
		time.sleep(0.005)
except KeyboardInterrupt:
	pass
servo_pwm.stop()
GPIO.cleanup()
