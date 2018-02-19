import serial
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

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
x = np.zeros(501)
y = np.zeros(501)
plt.ion()

ser.isOpen()

while True:
	
	while (ser.in_waiting() == 0):
		pass

	b = ser.read(size=5)
	bsync = b[0]
	if bsync == 255:
		b1i = b[1]
		b2i = b[2]
		b3i = b[3]
		b4i = b[4]
	

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
	
		if i == 0:
			os.system('clear')
			print('\nAnag1: '+"%.4f"%bi+' Dig1: '+str(d1)) # +' Dig2: '+str(d2)+' Par1: '+str(par1)+' Par2: '+str(par2))
			print('Anag2: '+"%.4f"%bj+' Dig2: '+str(d2))#+' Dig4: '+str(d4)+' Par3: '+str(par3)+' Par4: '+str(par4))
		
			plt.clf()
			plt.axis([0, 0.5, 0, 3])
			plt.plot(t, x, c='b')
			plt.plot(t, y, c='r')
			plt.pause(0.00001)
	
		i = (i+1)%40

	
ser.close()
exit()
