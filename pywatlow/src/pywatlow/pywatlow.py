import serial as ser
import crcmod
import struct
from binascii import unhexlify, hexlify

print('pywatlow file')

class PM3():
    '''
    Object representing a Watlow PM3 PID temperature controller
    '''
    def __init__(self, serial=None, port=None, timeout=0.5, address=1):
        self.timeout = timeout
        self.baudrate = 38400
        self.address = address
        if serial:
            self.port = serial.port
            self.serial = serial
        else:
            self.port = port
            self.open()

    def open(self):
        self.serial = ser.Serial(self.port, self.baudrate, timeout=self.timeout)

    def close(self):
        self.serial.flush()
        self.serial.close()

    def _f_to_c(self, f):
        return (f - 32) * (5/9)

    def _c_to_f(self, c):
        return (c * (9/5)) + 32

    def _headerCheckByte(self, headerBytes):
        '''
        Takes the full header byte array bytes[0] through bytes[6] of the full
        command and returns a check byte (bytearray of length one) using Watlow's
        algorithm

        Implementation relies on this post:
        https://reverseengineering.stackexchange.com/questions/8303/rs-485-checksum-reverse-engineering-watlow-ez-zone-pm
        '''
        crc_8_table = [
            0x00, 0xfe, 0xff, 0x01, 0xfd, 0x03, 0x02, 0xfc,
            0xf9, 0x07, 0x06, 0xf8, 0x04, 0xfa, 0xfb, 0x05,
            0xf1, 0x0f, 0x0e, 0xf0, 0x0c, 0xf2, 0xf3, 0x0d,
            0x08, 0xf6, 0xf7, 0x09, 0xf5, 0x0b, 0x0a, 0xf4,
            0xe1, 0x1f, 0x1e, 0xe0, 0x1c, 0xe2, 0xe3, 0x1d,
            0x18, 0xe6, 0xe7, 0x19, 0xe5, 0x1b, 0x1a, 0xe4,
            0x10, 0xee, 0xef, 0x11, 0xed, 0x13, 0x12, 0xec,
            0xe9, 0x17, 0x16, 0xe8, 0x14, 0xea, 0xeb, 0x15,
            0xc1, 0x3f, 0x3e, 0xc0, 0x3c, 0xc2, 0xc3, 0x3d,
            0x38, 0xc6, 0xc7, 0x39, 0xc5, 0x3b, 0x3a, 0xc4,
            0x30, 0xce, 0xcf, 0x31, 0xcd, 0x33, 0x32, 0xcc,
            0xc9, 0x37, 0x36, 0xc8, 0x34, 0xca, 0xcb, 0x35,
            0x20, 0xde, 0xdf, 0x21, 0xdd, 0x23, 0x22, 0xdc,
            0xd9, 0x27, 0x26, 0xd8, 0x24, 0xda, 0xdb, 0x25,
            0xd1, 0x2f, 0x2e, 0xd0, 0x2c, 0xd2, 0xd3, 0x2d,
            0x28, 0xd6, 0xd7, 0x29, 0xd5, 0x2b, 0x2a, 0xd4,
            0x81, 0x7f, 0x7e, 0x80, 0x7c, 0x82, 0x83, 0x7d,
            0x78, 0x86, 0x87, 0x79, 0x85, 0x7b, 0x7a, 0x84,
            0x70, 0x8e, 0x8f, 0x71, 0x8d, 0x73, 0x72, 0x8c,
            0x89, 0x77, 0x76, 0x88, 0x74, 0x8a, 0x8b, 0x75,
            0x60, 0x9e, 0x9f, 0x61, 0x9d, 0x63, 0x62, 0x9c,
            0x99, 0x67, 0x66, 0x98, 0x64, 0x9a, 0x9b, 0x65,
            0x91, 0x6f, 0x6e, 0x90, 0x6c, 0x92, 0x93, 0x6d,
            0x68, 0x96, 0x97, 0x69, 0x95, 0x6b, 0x6a, 0x94,
            0x40, 0xbe, 0xbf, 0x41, 0xbd, 0x43, 0x42, 0xbc,
            0xb9, 0x47, 0x46, 0xb8, 0x44, 0xba, 0xbb, 0x45,
            0xb1, 0x4f, 0x4e, 0xb0, 0x4c, 0xb2, 0xb3, 0x4d,
            0x48, 0xb6, 0xb7, 0x49, 0xb5, 0x4b, 0x4a, 0xb4,
            0xa1, 0x5f, 0x5e, 0xa0, 0x5c, 0xa2, 0xa3, 0x5d,
            0x58, 0xa6, 0xa7, 0x59, 0xa5, 0x5b, 0x5a, 0xa4,
            0x50, 0xae, 0xaf, 0x51, 0xad, 0x53, 0x52, 0xac,
            0xa9, 0x57, 0x56, 0xa8, 0x54, 0xaa, 0xab, 0x55
        ]

        # Watlow's header check byte algorithm:
        intCheck = ~crc_8_table[headerBytes[6] ^ crc_8_table[headerBytes[5] ^ \
                  crc_8_table[headerBytes[4] ^ crc_8_table[headerBytes[3] ^ \
                  crc_8_table[~headerBytes[2]]]]]] & (2**8-1)
        return bytes([intCheck])

    def _dataCheckByte(self, dataBytes):
        '''
        Takes the full data byte array, bytes[8] through bytes[13] of the full
        command and calculates the data check byte using BacNET CRC-16
        '''
        # CRC-16 with 0xFFFF as initial value, 0x1021 as polynomial, bit reversed
        crc_fun = crcmod.mkCrcFun(poly=0x11021, initCrc=0, rev=True, xorOut=0xFFFF)
        # bytes object packed using C-type unsigned short, little-endian:
        byte_str = struct.pack('<H', crc_fun(dataBytes))
        return byte_str

    def _buildReadRequest(self, dataParam):
        '''
        Takes the watlow parameter ID, converts to bytes objects, calls
        internal functions to calc check bytes, and assembles/returns the request
        byte array
        '''
        # Request Header:
        BACnetPreamble = '55ff'
        requestParam = '05'
        zone = str(9 + self.address)
        additionalHeader = '000006'
        hexHeader = BACnetPreamble + requestParam + zone + additionalHeader

        # Request Data Parameters
        additionalData = '010301'
        # Reformats data param from notation in the manual to hex
        # (e.g. '4001' to '04' and '001' to '0401')
        dataParam = format(int(dataParam), '05d')
        dataParam = hexlify(int(dataParam[:2]).to_bytes(1, 'big') + int(dataParam[2:]).to_bytes(1, 'big')).decode('utf-8')
        instance = '01'
        hexData = additionalData + dataParam + instance

        # Convert input strings to bytes:
        hexHeader = unhexlify(hexHeader)
        hexData = unhexlify(hexData)

        # Calculate check bytes:
        headerChk = self._headerCheckByte(hexHeader)
        dataChk = self._dataCheckByte(hexData)

        # Assemble request byte array:
        request = bytearray(hexHeader)
        request += bytearray(headerChk)
        request += bytearray(hexData)
        request += dataChk

        return request

    def _buildSetTempRequest(self, value):
        '''
        Takes the set point temperature value, converts to bytes objects, calls
        internal functions to calc check bytes, and assembles/returns the request
        byte array

        Much of this function is hard coded until I figure out how each
        part of the hex command is assembled. It is different than a normal read
        command
        '''
        # Request Header:
        BACnetPreamble = '55ff'
        requestParam = '05'
        zone = str(9 + self.address)
        additionalHeader = '00000a'
        hexHeader = BACnetPreamble + requestParam + zone + additionalHeader

        # Data portion of request (here the set point value is appended)
        hexData = '010407010108'

        value = struct.pack('>f', value)

        # Convert input strings to bytes:
        hexHeader = unhexlify(hexHeader)
        hexData = unhexlify(hexData) + value

        # Calculate check bytes:
        headerChk = self._headerCheckByte(hexHeader)
        dataChk = self._dataCheckByte(hexData)

        # Assemble request byte array:
        request = bytearray(hexHeader)
        request += bytearray(headerChk)
        request += bytearray(hexData)
        request += dataChk

        return request

    def _validateResponse(self, bytesResponse):
        '''
        Compares check bytes received in response to those calculated

        TODO: make sure this checks that the address in response is correct
        '''
        isValid = False
        # Evaluate headerChk as bytearray instead of as an int (which is how
        # python will interpret a single hex character)
        headerChkReceived = bytearray([bytesResponse[7]])
        dataCheckRecieved = bytesResponse[-2:]
        addressReceived = int(bytesResponse.hex()[8:10]) - 9
        if (headerChkReceived == self._headerCheckByte(bytesResponse[0:7]) and \
            dataCheckRecieved == self._dataCheckByte(bytesResponse[8:-2]) and \
            addressReceived == self.address):
            isValid = True
        return isValid

    def _parseResponse(self, bytesResponse):
        '''
        Takes the full response byte array and extracts the relevant data (e.g.
        current temperature), constructs response dict, and returns it
        '''
        print(bytesResponse, len(bytesResponse))
        try:
            if bytesResponse == b'' or bytesResponse == bytearray(len(bytesResponse)):
                raise Exception('Exception: No response at address {0}'.format(self.address))
            if not self._validateResponse(bytesResponse):
                print('Invalid Response at address {0}: '.format(self.address), hexlify(bytesResponse))
                raise Exception('Exception: Invalid response received from address {0}'.format(self.address))
        except Exception as e:
            #print(e)
            output = {
                        'address': self.address,
                        'data': None,
                        'error': e
                     }
        else:

            ieee_754 = hexlify(bytesResponse[-6:-2])
            #print('response: ', hexlify(bytesResponse))
            #print('ieee_754: ', ieee_754)
            data = struct.unpack('>f', unhexlify(ieee_754))[0]
            output = {
                        'address': self.address,
                        'data': self._f_to_c(data),
                        'error': None
                     }

        return output

    def readParam(self, param):
        '''
        Takes a parameter and writes data to the watlow controller at
        object's internal address

        Data parameters are split like so: 4001 --> '04' and '001' --> '0401' in hex

        Zone corresponds to the address parameter in setup (e.g. '10' = 1, '11' = 2, etc.)

        Returns a dict containing the response data and address
        '''
        request = self._buildReadRequest(param)
        print('read request add. ' + str(self.address) + ': ', hexlify(request), len(request))
        try:
            self.serial.write(request)
        except Exception as e:
            print('Exception: ', e)
        else:
            response = self.serial.read(21)
            print('read response add ' + str(self.address) + ': ', hexlify(response), len(response))
            output = self._parseResponse(response)
            return output

    def setTemp(self, value):
        '''
        Changes the watlow PM3 temperature setpoint

        Takes a value (in degrees C), builds request, writes to watlow PM3,
        receives and returns response object
        '''
        value = self._c_to_f(value)
        request = self._buildSetTempRequest(value)
        print('set request add. ' + str(self.address) + ': ', hexlify(request), len(request))

        try:
            self.serial.write(request)
        except Exception as e:
            print('Exception: ', e)
        else:
            bytesResponse = self.serial.read(20)
            print('set response add ' + str(self.address) + ': ', hexlify(bytesResponse), len(bytesResponse))
            output = self._parseResponse(bytesResponse)
            print('output: ', output)
            return output
