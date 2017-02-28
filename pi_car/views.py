'''
#=============================================================================
#     FileName: views.py
#         Desc: 
#       Author: wangheng
#        Email: wujiwh@gmail.com
#     HomePage: http://wangheng.org
#      Version: 0.0.1
#   LastChange: 2015-01-14 13:46:29
#      History:
#=============================================================================
'''
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
from pi_car import app
import re
import RPi.GPIO as GPIO
import time
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)
fl_pin = 7  # Front Light

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(fl_pin, GPIO.OUT, initial=False)
#GPIO.setup(a_1,GPIO.OUT,initial = False)
#GPIO.setup(a_2,GPIO.OUT,initial = False)
#GPIO.setup(b_1,GPIO.OUT,initial = False)
#GPIO.setup(b_2,GPIO.OUT,initial = False)

@app.route('/')
def show_index():
	return render_template('home.html')

@app.route("/login", methods=["GET", "POST"])                                   
def login():                                                                    
	if request.method=="GET":                                                   
		return "get"+request.form["user"]
	elif request.method=="POST":                                                
		return "post"

@app.route('/ctl',methods=['GET','POST'])
def ctrl_id():
	if request.method == 'POST':
		id=request.form['id']

		if id == 't_left':
			t_left()
			return "left"
		elif id == 't_right':
			t_right()
			return "right"
		elif id == 't_up':
			t_up()
			return "up"
		elif id == 't_down':
			t_down()
			return "down"
		elif id == 't_stop':
			t_stop()
			return "stop"
	return redirect(url_for('show_index'))

@app.route('/ctlcam',methods=['GET','POST'])
def ctrl_cam():
        if request.method == 'POST':
        	anglex = int(str(request.form['anglex']))
		angley = int(str(request.form['angley']))
		ser.write("C%03d%03d"%(anglex,angley))
		return "camx:" + str(anglex) + " camy:" + str(angley)
	return redirect(url_for('show_index'))

@app.route('/ctlspeed',methods=['GET','POST'])
def ctrl_speed():
        if request.method == 'POST':
        	sa = int(str(request.form['speedA']))
		sb = int(str(request.form['speedB']))
		ser.write("E%03d%03d"%(sa,sb))
		return "speedA:" + str(sa) + " speedB:" + str(sb)
	return redirect(url_for('show_index'))

@app.route('/ctllight',methods=['GET','POST'])
def ctrl_light():
	if request.method == 'POST':
		front_light = int(str(request.form['frontLight']))
		GPIO.output(fl_pin, front_light)
		return "Front Light:" + str(front_light)
	return redirect(url_for('show_index'))

def t_stop():
	ser.write("S");
def t_up():
	ser.write("F");
def t_down():
	ser.write("B");
def t_left():
	ser.write("L");
def t_right():
	ser.write("R");
