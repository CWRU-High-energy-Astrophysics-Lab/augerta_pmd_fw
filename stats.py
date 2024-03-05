import serial
import pandas as pd
import numpy as np
import time
import datetime 
import os
'''
This code receives data from arduinovs.ino and interprets it and saves it in files named Hourly.csv, Daily.csv, Weekly.csv
The variables below (baudrate, port, sensorAmount, dataInterval(sec)) should be set properly before running. If you change anything in
the input sequence, you may have to change same parts of this code as well as it directly disects the data it receives.
'''

baudrate = 115200                                                                                 #Baudrate from arduinovs.ino
port = "/dev/ttyUSB1"                                                                                     #The port that the transmitter in connected to
sensorAmount = 11                                                                                 #The amount of sensors connected to the transmitter
dataInterval = 1                                                                                 #The interval between data collections
 #Gets the time/date for use
check=0
current_sensor=0
ser= serial.Serial()
ser.baudrate = baudrate
ser.port = port
ser.open()
hour_collect=[None for i in range(0,12)]
hour_collect[0]=pd.DataFrame({'Temp':[]})
pause=False
for  i  in range(1,12):
	hour_collect[i]=pd.DataFrame({"Bus":[],"Shunt":[], "Load":[],"Current":[],"Power":[]})
ser.flush()
while(True):
	line=ser.readline()
	try:
		if b'Temp' in line:
			#print(line[6:10])
			hour_collect[0].loc[len(hour_collect[0].index)]=[float(line[6:10])]
			#print(len(hour_collect[0].index))
		
		elif b'Current Sensor' in line:
			current_sensor= int(line[-5:-3])
		
			BusV=float(ser.readline().split(b':')[1][:-3])
			ShuntV=float(ser.readline().split(b':')[1][:-4])
			LoadV=float(ser.readline().split(b':')[1][:-3])
			Current=float(ser.readline().split(b':')[1][:-4])
			Power=float(ser.readline().split(b':')[1][:-4])
			hour_collect[current_sensor].loc[len(hour_collect[current_sensor].index)]=[BusV,ShuntV,LoadV,Current,Power]
			#print(len(hour_collect[current_sensor].index))
		#print(hour_collect[1].describe())
	except:
		pass
	now=datetime.datetime.now()
	if now.minute == check+1:
		pause=False
	if now.minute == check and pause==False:
		pause =True
		if now.hour == 0 or not os.path.exists(f"/home/pi/augerta_pmd_fw/FrodoPower_{now.month}_{now.day}_{now.year}"):
			os.chdir("/home/pi/augerta_pmd_fw")
			os.mkdir(f"FrodoPower_{now.month}_{now.day}_{now.year}")
			os.chdir(f"FrodoPower_{now.month}_{now.day}_{now.year}")
		os.chdir(f"/home/pi/augerta_pmd_fw/FrodoPower_{now.month}_{now.day}_{now.year}")
		try:
			os.mkdir("hour"+str(now.hour-1))
		except:
			pass
		os.chdir("hour"+str(i))
		for i in range(len(hour_collect)):
			hour_collect[i].describe().to_csv("Sensor"+str(i)+".csv")
			

		print("File Saved")
		hour_collect=[None for i in range(0,12)]
		hour_collect[0]=pd.DataFrame({'Temp':[]})
		for  i  in range(1,12):
       			 hour_collect[i]=pd.DataFrame({"Bus":[],"Shunt":[], "Load":[],"Current":[],"Power":[]})

