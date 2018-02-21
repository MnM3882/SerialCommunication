import serial
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import time
#import scipy

stopsignal = False

def stopevent(event):
	global stopsignal
	stopsignal = True

def scope():
	# configure the serial connections (the parameters differs on the device you are connecting to)
	ser = serial.Serial(
	    port='/dev/ttyUSB0',#'/dev/ttyACM0',
	    baudrate=115200,
	    parity=serial.PARITY_NONE,
	    stopbits=serial.STOPBITS_ONE,
	    bytesize=serial.EIGHTBITS
	)
	global stopsignal
	try:
		if ser.isOpen():
			ser.close()	
		ser.open()
	except Exception:
		print("Error abriendo el puerto.")
		exit()

	if ser.isOpen():
		i = 0
		t = np.linspace(0, 0.5, 501)
		x = np.zeros(501)
		y = np.zeros(501)

		fig = plt.figure()
		ax = fig.add_subplot(1,1,1)
		ax.axis([0, 0.5, 0, 3])
		ax.set_title('Senales analogicas en tiempo real')
		lines1, = ax.plot(t, x, c='b')
		lines2, = ax.plot(t, y, c='r')
		
		#cid = lines1.figure.canvas.mpl_connect('button_press_event', stopevent)
		#cid = lines2.figure.canvas.mpl_connect('button_press_event', stopevent)
		cid = lines1.figure.canvas.mpl_connect('close_event', stopevent)
		cid = lines2.figure.canvas.mpl_connect('close_event', stopevent)
		
		
		
		plt.ion()
		plt.show()

		fig.canvas.draw()

		os.system('clear')
		ser.reset_input_buffer()
	
		while not stopsignal:
	
			b = ser.read(size=4)
		
		
			b1i = b[0]
			b2i = b[1]
			b3i = b[2]
			b4i = b[3]
			if b1i >= 128:
			
				d1 = (b1i & 0x20) >> 5
				d2 = (b3i & 0x20) >> 5

				bi = 3*(((b1i & 0x1F) << 7) + (b2i & 0x7F))/4095
				bj = 3*(((b3i & 0x1F) << 7) + (b4i & 0x7F))/4095

				x = np.delete(x,0)
				x = np.append(x,bi)
	
				y = np.delete(y,0)
				y = np.append(y,bj)

				if (i == 0 or tt == True) and not stopsignal:
					tt = True
					if ser.in_waiting == 0:
						now = time.time()
					
						os.system('clear')
						print('\nAnag1: '+"%.4f"%bi+' Dig1: '+str(d1))
						print('Anag2: '+"%.4f"%bj+' Dig2: '+str(d2))
		
						lines1.set_ydata(x)
						lines2.set_ydata(y)
						fig.canvas.draw()

						plt.pause(0.001)

						tt = False
	
				i = (i+1)%100
			
			else:
				print("Bad sync")
				ser.reset_input_buffer()

		ser.close()
		os.system('clear')
	plt.close()
	stopsignal = False

def storedata():
	# configure the serial connections (the parameters differs on the device you are connecting to)
	ser = serial.Serial(
	    port='/dev/ttyUSB0',#'/dev/ttyACM0',
	    baudrate=115200,
	    parity=serial.PARITY_NONE,
	    stopbits=serial.STOPBITS_ONE,
	    bytesize=serial.EIGHTBITS
	)
	global stopsignal
	try:
		if ser.isOpen():
			ser.close()	
		ser.open()
	except Exception:
		print("Error abriendo el puerto.")
		exit()

	if ser.isOpen():
		
		os.system('clear')
		ser.reset_input_buffer()
		
		with open("anag1.m", 'w') as fx, open("anag2.m", 'w') as fy, open("dig1.m", 'w') as fd1, open("dig2.m", 'w') as fd2, open("error_report.txt", 'w') as fe:

			for i in range(1000):
	
				b = ser.read(size=4)
		
				b1i = b[0]
				b2i = b[1]
				b3i = b[2]
				b4i = b[3]
				if b1i >= 128:
			
					d1 = (b1i & 0x20) >> 5
					d2 = (b3i & 0x20) >> 5

					bi = 3*(((b1i & 0x1F) << 7) + (b2i & 0x7F))/4095
					bj = 3*(((b3i & 0x1F) << 7) + (b4i & 0x7F))/4095

					fx.write("%f\n"%bi)
					fy.write("%f\n"%bj)
					
					fd1.write("%d\n"%d1)
					fd2.write("%d\n"%d2)
			
				else:
					fx.write("%f\n"%bi)
					fy.write("%f\n"%bj)
					
					fd1.write("%d\n"%d1)
					fd2.write("%d\n"%d2)

					fe.write("Error en la posicion %d"%i)

		ser.close()
		os.system('clear')
