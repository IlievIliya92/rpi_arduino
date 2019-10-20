import serial

ser = ""

def initSerial():
	global ser
	
	ser = serial.Serial(
		port='/dev/ttyACM1',
		baudrate=9600,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout = 10
	)
	print("Serial Initialized.")
	
def sendData(data):
	data += '*'
	ser.write(data.encode('utf-8')) 
