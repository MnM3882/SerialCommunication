import serial
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import time
import select

stopsignal = False

def stopevent(event):
	global stopsignal
	stopsignal = True

def scope():
	# configure the serial connections (the parameters differs on the device you are connecting to)
	ser = serial.Serial(
	    port='/dev/ttyACM0',
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
		ax.set_title('Presione ENTER para detener esta funcion')
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
			
				if ser.in_waiting > 500:
					print(ser.in_waiting)
				#ser.reset_input_buffer()
			
				#par1 = b1i >> 7
				#par2 = b2i >> 7
				#par3 = b3i >> 7
				#par4 = b4i >> 7
	

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
						print('\nAnag1: '+"%.4f"%bi+' Dig1: '+str(d1)) # +' Dig2: '+str(d2)+' Par1: '+str(par1)+' Par2: '+str(par2))
						print('Anag2: '+"%.4f"%bj+' Dig2: '+str(d2))#+' Dig4: '+str(d4)+' Par3: '+str(par3)+' Par4: '+str(par4))
		
						#plt.clf()
						#plt.axis([0, 0.5, 0, 3])
						#plt.plot(t, x, c='b')
						#plt.plot(t, y, c='r')
						#ax.lines.pop(0)
						#ax.lines.pop(0)
						#lines1 = ax.plot(t, x, c='b')
						#lines2 = ax.plot(t, y, c='r')
						lines1.set_ydata(x)
						lines2.set_ydata(y)
						fig.canvas.draw()

						plt.pause(0.001)
					
						#print("Presione 'Enter' para salir")

						print(now-time.time())	
						#print('\n\n\n')
						tt = False
	
				i = (i+1)%100
			
			
				#print(now-time.time())
			else:
				print("Bad sync")
				ser.reset_input_buffer()

		ser.close()
		#input()	
		os.system('clear')
	plt.close()
	stopsignal = False
