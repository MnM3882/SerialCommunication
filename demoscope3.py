import serial
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import time

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

i = 0
t = np.linspace(0, 0.5, 501)
x = np.ones(501) #np.zeros(101)
y = 2*np.ones(501) #np.zeros(101)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.axis([0, 0.5, 0, 3])
lines1, = ax.plot(t, x, c='b')
lines2, = ax.plot(t, y, c='r')

plt.ion()
plt.show()

fig.canvas.draw()

'''
try:
	ser.open()
except(Exception, e):
	print("Error abriendo el puerto.")
	exit()
''' 
if ser.isOpen():

	ser.reset_input_buffer()
	
	while 1:
	
	#	while (ser.in_waiting == 0):
	#		print(ser.in_waiting)

		b = ser.read(size=4)
		
		
		b1i = b[0]
		b2i = b[1]
		b3i = b[2]
		b4i = b[3]
		if b1i >= 128:
			
			#if ser.in_waiting > 4:
			#	print(ser.in_waiting)
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

			if i == 0 or tt == True:
				tt = True
				if ser.in_waiting == 0:
					#os.system('clear')
					#print('\nAnag1: '+"%.4f"%bi+' Dig1: '+str(d1)) # +' Dig2: '+str(d2)+' Par1: '+str(par1)+' Par2: '+str(par2))
					#print('Anag2: '+"%.4f"%bj+' Dig2: '+str(d2))#+' Dig4: '+str(d4)+' Par3: '+str(par3)+' Par4: '+str(par4))
		
					#plt.clf()
					#plt.axis([0, 0.5, 0, 3])
					#plt.plot(t, x, c='b')
					#plt.plot(t, y, c='r')
					#ax.lines.pop(0)
					#ax.lines.pop(0)
					#lines1 = ax.plot(t, x, c='b')
					#lines2 = ax.plot(t, y, c='r')
					now = time.time()
					lines1.set_ydata(x)
					lines2.set_ydata(y)
					fig.canvas.draw()
					print(now-time.time())	
					#plt.pause(0.00001)
					tt = False
	
			i = (i+1)%100
			
			
			#print(now-time.time())
		else:
			print("Bad sync")
			ser.reset_input_buffer()

ser.close()
exit()
