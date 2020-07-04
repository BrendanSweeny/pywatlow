from pywatlow.watlow import Watlow
import serial

ser = serial.Serial()
ser.port = 'COM5'
ser.baudrate = 38400
ser.timeout = 0.5
ser.open()

watlow_one = Watlow(serial=ser, address=1)
watlow_two = Watlow(serial=ser, address=2)
print(watlow_one.readParam(7001))
print(watlow_two.readParam(4001))
