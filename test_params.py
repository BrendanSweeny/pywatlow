from pywatlow.watlow import Watlow
import struct
from binascii import hexlify
from binascii import unhexlify

watlow = Watlow(port='COM5', address=1)

param_default_dict = {
    4005: 'Thermocouple or Thermistor', # Sensor Type
    4007: 2, # RTD Leads
    7001: '??', # Setpoint
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

param_default_dict_two = [
    (4005, 95, int, '55FF0511030009CF01040405010F01005F26D8'), # Sensor Type
    (4007, 1, int, '55FF0511030009CF01040407010F0100018B6B'), # RTD Leads
    (4042, 75, int, '55FF0511030009CF0104042A010F01004B6A36'), # Units
    (4015, 0.0, float, '55FF051100000A650104040F0108000000009B21'), # Scale Low
    (4016, 20.0, float, '55FF051100000A6501040410010841A000007D88'), # Scale High
    (4017, 0.0, float, '55FF051100000A65010404110108000000007312'), # Range Low
    (4018, 9999.0, float, '55FF051100000A65010404120108461C3C0004D8'), # Range High
    (4030, 62, int, '55FF0511030009CF0104041E010F01003E3CC5'), # Process error enable
    (4031, 0.0, float, '55FF051100000A650104041F0108000000005294'), # Process error low value
    (4037, 1449, int, '55FF0511030009CF01040425010F0105A947B1'), # Resistance Range of thermistor
    (4014, 0.5, float, '55FF051100000A650104040E01083F0000004540'), # Filter
    (4028, 62, int, '55FF0511030009CF0104041C010F01003E6ACD'), # Input Error Latching
    (4020, 105, int, '55FF0511030009CF01040414010F01006908CA'), # Display precision
    (4012, 0.0, float, '55FF051100000A650104040C010800000000F589'), # Calibration offset
    (34005, 62, int, '55FF0511030009CF01042205010F01003EE791'), # Linearization function
    (34029, 1539, int, '55FF0511030009CF0104221D010F010603B94C'), # Linearization Units
    (34008, 0.0, float, '55FF051100000A6501042208010800000000C24D'), # Linearization input point 1
    (34018, 0.0, float, '55FF051100000A65010422120108000000005C11'), # Linearization output point 1
    (26021, 62, int, '55FF0511030009CF01041A15010F01003EF1DB'), # Process Value function
    (26028, 1671, int, '55FF0511030009CF01041A1C010F0106871882'), # Process Value Pressure Units
    (26029, 1677, int, '55FF0511030009CF01041A1D010F01068D6929'), # Altitude Units
    (26030, 14.7, float, '55FF051100000A6501041A1E0108416B3333C7D9'), # Barometric Pressure
    (26026, 0.0, float, '55FF051100000A6501041A1A010800000000840F'), # Filter
    (6001, 68, int, '55FF0511030009CF01040601010F0100446351'), # Digital I/O Direction
]


'''for param in param_default_dict:
    #print((unhexlify(watlow._intDataParamToHex(param)), param))
    print(param, watlow.readParam(param)['data'])
    #print(param, watlow._formatDataParam(param))'''
'''for i in param_default_dict_two:
    print(i[0], watlow.setParam(i[0], i[1], i[2]))'''

#print(watlow.setParam(4001, 100, float))
#print(hexlify(b'U\xff\x06\x00\x10\x00\x02\x8f\x02\x85R\xef'))
#print(hexlify(b'U\xff\x06\x00\x10\x00\nv\x02\x04\x07\x01\x01\x08C\x16\x00\x0059'))
#print(7001, watlow.readParam(7001))
#print(watlow.setTemp(200))
print(7001, watlow.setParam(7001, 392))
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

# Possible Int set request:
# 55 FF 05 10 00 00 0A EC 01 04 08 03 01 0F 01 00 47 8F ED
#print(hexlify(watlow._dataCheckByte(unhexlify('01040803010F010047'))))
#print(watlow.writeBytes(8003))
#print(watlow.setTemp(100))
#print(watlow.setParam(7001, 80))
#print(watlow.setParam(8003, 71))
#print(watlow.readParam(4001))
#print(watlow.setTemp(100))
#print(unhexlify(watlow._intDataParamToHex(26029)))
#print(unhexlify(watlow._intDataParamToHex(34018)))
#print(watlow._byteDataParamToInt(b'\x08\x03'))
#print(watlow._byteDataParamToInt(b'\x07\x01'))
#print(watlow._byteDataParamToInt(b'\x1a\x1d'))
#print(watlow._byteDataParamToInt(b'"\x12'))
'''for i in range(0, 16):
    print('01' + hexlify(bytes([i])).decode('utf-8'))
    print(watlow.writeBytes(8003, hexlify(bytes([i])).decode('utf-8')))'''
#print(hexlify((71).to_bytes(2, 'big')))
#print(watlow.writeBytes(7001))

# Requests so far that garnered a response:
# 55 ff 05 10 00 00 0a ec 01 04 08 03 01 08 00 00 00 47 d8 9d **** 55 FF 06 00 10 00 02 8F 02 85 52 EF
# 55 ff 05 10 00 00 0a ec 01 04 08 03 01 01 00 00 00 47 bc cc **** 55 FF 06 00 10 00 02 8F 02 85 52 EF
# 55 ff 05 10 00 00 0a ec 01 04 08 03 01 08 01 00 00 47 63 81 **** 55 FF 06 00 10 00 02 8F 02 85 52 EF
# 55 ff 05 10 00 00 0a ec 01 04 08 03 01 0f 00 00 00 47 d8 9d **** 55 FF 06 00 10 00 02 8F 02 86 C9 DD
# 55 ff 05 10 00 00 0a ec 01 04 08 03 01 0f 01 00 00 47 bf b1 **** 55 FF 06 00 10 00 02 8F 02 86 C9 DD
# 55 ff 05 10 00 00 0a ec 01 03 08 03 01 08 01 00 00 47 81 68 **** 55 FF 06 00 10 00 02 8F 02 83 64 8A
# 55 ff 05 10 00 00 0a ec 01 03 08 03 01 08 00 00 00 47 3a 74 **** 55 FF 06 00 10 00 02 8F 02 83 64 8A
# 55 ff 05 10 00 00 0a ec 01 03 08 03 01 0f 00 00 00 47 e6 44 **** 55 FF 06 00 10 00 02 8F 02 83 64 8A
# 55 ff 05 10 00 00 0a ec 01 03 08 03 01 0f 01 00 00 47 5d 58 **** 55 FF 06 00 10 00 02 8F 02 83 64 8A
# 55 ff 05 10 00 00 0a ec 01 03 08 03 01 08 01 00 00 47 81 68 **** 55 FF 06 00 10 00 02 8F 02 83 64 8A
# 55 ff 05 10 00 00 0a ec 01 05 08 03 01 08 01 00 00 47 9e cc **** 55 FF 06 00 10 00 05 73 02 05 08 03 00 02 5B
# 55 ff 05 10 00 00 0a ec 01 05 08 03 01 08 00 00 00 47 25 d0 **** 55 FF 06 00 10 00 05 73 02 05 08 03 00 02 5B
# 55 ff 05 10 00 00 0a ec 01 05 08 03 01 0f 01 00 00 47 42 fc **** 55 FF 06 00 10 00 05 73 02 05 08 03 00 02 5B
# 55 ff 05 10 00 00 0a ec 01 05 01 08 03 01 0f 01 00 47 b3 bb **** 55 FF 06 00 10 00 05 73 02 05 01 08 00 B4 23
# 55 ff 05 10 00 00 0a ec 01 04 01 08 03 01 0f 01 00 47 4e f6 **** 55 FF 06 00 10 00 02 8F 02 80 FF B8

# ***For data param 8003, this is the winner:***
# 55 ff 05 10 03 00 09 46 01 04 08 03 01 0f 01 00 47 8f ed ****    55 FF 06 03 10 00 09 EF 02 04 08 03 01 0F 01 00 47 88 3B

# ***For 34005, this works:***
# 55 ff 05 10 03 00 09 46 01 04 22 05 01 0f 01 00 3e e7 91 ****    55 FF 06 03 10 00 09 EF 02 04 22 05 01 0F 01 00 3E E0 47

# 55 ff 05 10 00 00 0a ec 01 04 08 03 01 0f 01 00 47 8f ed **** no response
# 55 ff 05 10 00 00 06 e8 01 03 08 03 01 08 01 00 00 47 81 68 **** no response
# 55 ff 05 10 00 00 06 e8 01 04 01 08 03 01 0f 01 00 47 4e f6 **** no response
