import serial
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
port = "/dev/ttyUSB1"

scope= serial.Serial(port,baudrate=115200)

while(True):
	print(scope.read_until(b"\r\n\r\n"))
	print("break") 
