import serial

# Port below is for bluetooth
#hub=serial.Serial(port="COM6", baudrate=115200)

# Port below is for USB
hub=serial.Serial(port="COM5", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

#file=open('sensor_log.txt','r')

#list_string = list(file)

#for s in list_string:
#    print(s)

hub.write(b'\x03')
hub.write(b"file = open('sensor_log.txt','r')\r")
hub.write(b"for line in file:\r")
hub.write(b"print(line, end='')\r")
hub.write(b"\b")
hub.flush()
hub.write(b"\r")
print(hub.read_until(expected='>>>'))


#for i in range (10):
#    print(hub.readline())
#print("aaaa")