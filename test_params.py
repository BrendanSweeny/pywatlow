from pywatlow.watlow import Watlow
import struct
from binascii import hexlify
from binascii import unhexlify

watlow = Watlow(port='COM5', address=1)

param_default_dict = {
    4005: 'Thermocouple or Thermistor', # Sensor Type
    4007: 2, # RTD Leads
    4042: 'Process', # Units
    4015: 0.0, # Scale Low
    4016: 20.0, # Scale High
    4017: 0.0, # Range Low
    4018: 20.0, # Range High
    4030: 'Off', # Process error enable
    4031: 0.0, # Process error low value
    4037: '40K', # Resistance Range of thermistor
    4014: 0.5, # Filter
    4028: 'Off', # Input Error Latching
    4020: 'Whole', # Display precision
    4012: 0.0, # Calibration offset
    4001: '----', # Process temperature
    4002: '----', # Input error
    34005: 'Off', # Linearization function
    34029: 'Source', # Linearization Units
    34008: 0.0, # Linearization input point 1
    34018: 0.0, # Linearization output point 1
    26021: 'Off', # Process Value function
    26028: 'PSI', # Process Value Pressure Units
    26029: 'Hft', # Altitude Units
    26030: 14.7, # Barometric Pressure
    26026: 0.0, # Filter
    6001: 'Output', # Digital I/O Direction
    8003: 'PID', # Heat Algorithm
}


#for param in param_default_dict:
    #print(param, watlow.readParam(param)['data'])
    #print(param, watlow._formatDataParam(param))
#print(hexlify(b'U\xff\x06\x00\x10\x00\x02\x8f\x02\x85R\xef'))
#print(hexlify(b'U\xff\x06\x00\x10\x00\nv\x02\x04\x07\x01\x01\x08C\x16\x00\x0059'))
#print(7001, watlow.readParam(7001))
print(watlow.setTemp(200))
#print(7001, watlow.setParam(7001, 150))
#print(7001, watlow.readParam(7001))

#print(struct.unpack('>f', unhexlify(b'0f01003e'))[0])
#print(watlow.readParam(7001))
#print(watlow.readParam(4001))
#print(watlow.readParam(8003))
#print(watlow.readParam(4037))


# Example Responses and the corresponding int value
# Header                H check  ??     Param    ??        Hex          D Chk
# 55 ff 06 00 10 00 0a - 76 02 - 03 01 - 06 01 - 01 0f 01 - 00 44       - 29 d7, 6001, 0044, 68
# 55 ff 06 00 10 00 0a - 76 02 - 03 01 - 08 03 - 01 0f 01 - 00 3e       - 83 85, 8003, 003e, 62
# 55 ff 06 00 10 00 0a - 76 02 - 03 01 - 1a 1d - 01 0f 01 - 06 8d       - 23 af, 26029, 068d, 1677
# 55 ff 06 00 10 00 0a - 76 02 - 03 01 - 04 05 - 01 0f 01 - 00 5f       - 6c 5e, 4005, 005f, 95
# 55 ff 06 00 10 00 0a - 76 02 - 03 01 - 04 07 - 01 0f 01 - 00 01       - c1 ed, 4007, 0001, 1
# 55 ff 06 00 10 00 0a - 76 02 - 03 01 - 04 25 - 01 0f 01 - 05 a9       - 0d 37, 4037, 05a9, 1449
# 55 ff 06 00 10 00 0a - 76 02 - 03 01 - 1a 1d - 01 0f 01 - 06 8d       - 23 af, 26029, 068d, 1677
# 55 ff 06 00 10 00 02 - 8f 02 - 84                                     - db fe, 25030, This appears to be the response to a nonexistent param
# 55 ff 06 00 10 00 0b - 88 02 - 03 01 - 07 01 - 01 08    - 43 03 00 00 - ac 1c, 7001, 43030000, 131.0
# 55 ff 06 00 10 00 0b - 88 02 - 03 01 - 04 01 - 01 08    - 45 1e 26 8c - 8b 9e, 4001, 451e268c, 2530.4091796875
# 55 ff 06 00 10 00 0b - 88 02 - 03 01 - 1a 1e - 01 08    - 41 6b 33 33 - 1f 34, 26030, 416b3333, 14.699999809265137
# 55 ff 06 00 10 00 0b - 88 02 - 03 01 - 1a 1a - 01 08    - 00 00 00 00 - 5c e2, 26026, 00000000, 0.0

# Response to set temp request
# 55 ff 06 00 10 00 0a - 76 - 02 04 - 07 01 - 01 08 - 43 16 00 00   - 35 39
# 55 ff 06 00 10 00 0a - 76 - 02 04 - 07 01 - 01 08 - 43 54 00 00 - fb 8a, 7001, 43540000

# 55 ff 06 00 10 00 02 - 8f 02 - 85                                     - 52 ef

# Set Requests that work:
# 55 FF 05 10 00 00 0A - EC 01 - 04    - 07 01 - 01 08    - 42 A0 00 00 - 7C 0D
