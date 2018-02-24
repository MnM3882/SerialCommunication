import serial
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import time
import scipy.fftpack
import pandas as pd

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
		ax.axis([0, 0.5, 0, 5])
		ax.set_title('Senales analogicas en tiempo real')
		lines1, = ax.plot(t, x, c='b', alpha = 0.7)
		lines2, = ax.plot(t, y, c='r', alpha = 0.7)
		
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

				bi = (((b1i & 0x1F) << 7) + (b2i & 0x7F))/819
				bj = (((b3i & 0x1F) << 7) + (b4i & 0x7F))/819

				x = np.delete(x,0)
				x = np.append(x,bi)
	
				y = np.delete(y,0)
				y = np.append(y,bj)

				if (i == 0 or tt == True) and not stopsignal:
					tt = True
					if ser.in_waiting == 0:
						now = time.time()
					
						os.system('clear')
						print('Canal analogico 1: '+"%.4f"%bi+'\tCanal digital 1: '+str(d1)+'\n')
						print('Canal analogico 2: '+"%.4f"%bj+'\tCanal digital 2: '+str(d2))
		
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
		
		with open("anag1.csv", 'w') as fx, open("anag2.csv", 'w') as fy, open("dig1.csv", 'w') as fd1, open("dig2.csv", 'w') as fd2, open("error_report.txt", 'w') as fe:

			for i in range(1000):
	
				b = ser.read(size=4)
		
				b1i = b[0]
				b2i = b[1]
				b3i = b[2]
				b4i = b[3]
				if b1i >= 128:
			
					d1 = (b1i & 0x20) >> 5
					d2 = (b3i & 0x20) >> 5

					bi = (((b1i & 0x1F) << 7) + (b2i & 0x7F))/819
					bj = (((b3i & 0x1F) << 7) + (b4i & 0x7F))/819

					fx.write("%f\n"%bi)
					fy.write("%f\n"%bj)
					
					fd1.write("%d\n"%d1)
					fd2.write("%d\n"%d2)
			
				else:
					d1 = (b1i & 0x20) >> 5
					d2 = (b3i & 0x20) >> 5

					bi = (((b1i & 0x1F) << 7) + (b2i & 0x7F))/819
					bj = (((b3i & 0x1F) << 7) + (b4i & 0x7F))/819

					fx.write("%f\n"%bi)
					fy.write("%f\n"%bj)
					
					fd1.write("%d\n"%d1)
					fd2.write("%d\n"%d2)

					fe.write("Error en la posicion %d"%i)

		ser.close()
		os.system('clear')

def plotsignal():
	t = np.linspace(0.0, 0.999, 1000)
	x = pd.read_csv('anag1.csv', header=None, squeeze = True).values
	y = pd.read_csv('anag2.csv', header=None, squeeze = True).values
	d1 = pd.read_csv('dig1.csv', header=None, squeeze = True).values
	d2 = pd.read_csv('dig2.csv', header=None, squeeze = True).values
	plt.plot(t, x, c='b', alpha = 0.7)
	plt.plot(t, y, c='r', alpha = 0.7)
	plt.plot(t, d1, c='g', alpha = 0.5)
	plt.plot(t, d2, c='y', alpha = 0.5)
	plt.ion()
	plt.show()
	os.system('clear')

def plotfourier():
	t = np.linspace(0.0, 0.999, 1000)
	x = pd.read_csv('anag1.csv', header=None, squeeze = True).values
	y = pd.read_csv('anag2.csv', header=None, squeeze = True).values
	xf = scipy.fftpack.fft(x)
	yf = scipy.fftpack.fft(y)
	f = np.linspace(0.0, 1.0/(2.0*0.999/1000), 1000/2)

	fig, ax = plt.subplots()
	ax.plot(f, 2.0/1000 * np.abs(xf[:1000//2]), c='b', alpha = 0.7)
	ax.plot(f, 2.0/1000 * np.abs(yf[:1000//2]), c='r', alpha = 0.7)
	plt.ion()
	plt.show()
	os.system('clear')

def plothistogram():
	x = pd.read_csv('anag1.csv', header=None, squeeze = True)
	y = pd.read_csv('anag2.csv', header=None, squeeze = True)
	d1 = pd.read_csv('dig1.csv', header=None, squeeze = True)
	d2 = pd.read_csv('dig2.csv', header=None, squeeze = True)
	x.plot.hist(color='b', alpha=0.7)
	y.plot.hist(color='r', alpha=0.7)
	d1.plot.hist(color='g', alpha=0.5)
	d2.plot.hist(color='y', alpha=0.5)
	plt.ion()
	plt.show()
	os.system('clear')
	print('Canal analogico 1:')
	print(x.describe())
	print('\nCanal analogico 2:')
	print(y.describe())

# Punto blanco -> Cable negro
