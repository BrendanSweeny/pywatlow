import unittest
import sys
import os

sys.path.append('../')

from pywatlow import PM3
from binascii import unhexlify

class TestWatlow(unittest.TestCase):
    '''
    Test suite for the PM3 class
    * Each command was varified with a response from Watlow PM3
    * Each response was a real response from a Watlow PM3
    '''
    def setUp(self):
        self.test_pm3_address1 = PM3(serial=None)
        self.test_pm3_address2 = PM3(serial=None, address=2)

    def test_dataCheckByte(self):
        '''
        Test that the correct check byte is calculated from the data portion
        of the hex command

        _dataCheckByte is the only function scored in this test
        '''
        test_data = {
            # Request, Address 1, '4001'
            '55ff0510000006e8010301040101e399': b'\xe3\x99',
            # Request, Address 2, '4001'
            '55ff051100000661010301040101e399': b'\xe3\x99',
            # Request, Address 2, '7001'
            '55ff0511000006610103010701018776': b'\x87\x76',
            # Responses (not necessarily from requests above)
            # Not necessary for function to calculate below correctly in practice
            '55FF060010000B8802030104010108468F3638DD0E': b'\xdd\x0e',
            '55ff060010000b8802030104010108468f3abe4346': b'\x43\x46',
            '55ff060011000b1002030104010108468f393a07ae': b'\x07\xae',
            '55ff060011000b100203010701010842960000d3b0': b'\xd3\xb0'
        }

        for hexCommand in test_data:
            # Assert that the key passed to _dataCheckByte results in the
            # corresponding test_data value:
            self.assertEqual(self.test_pm3_address1._dataCheckByte(unhexlify(hexCommand)[8:-2]), test_data[hexCommand], msg='{0}'.format(hexCommand))
            # Assert that the check byte length is equal to two:
            self.assertTrue(len(self.test_pm3_address1._dataCheckByte(unhexlify(hexCommand)[8:-2])) == 2, msg='{0}'.format(hexCommand))
            # Assert that the result is an instance of type 'bytes'
            self.assertIsInstance(self.test_pm3_address1._dataCheckByte(unhexlify(hexCommand)[8:-2]), bytes, msg='{0}'.format(hexCommand))

    def test_headerCheckByte(self):
        '''
        Tests that the correct check byte is calculated from the header
        portion of the hex command

        Watlow zone/address is the only parameter changed in the header by users

        _headerCheckByte is the only function scored by this test
        '''
        test_data = {
            # Request, Address 1, '4001'
            '55ff0510000006e8010301040101e399': b'\xe8',
            # Request, Address 2, '4001'
            '55ff051100000661010301040101e399': b'\x61',
            # Request, Address 2, '7001'
            '55ff0511000006610103010701018776': b'\x61',
            # Responses (not necessarily from requests above)
            # Not necessary for function to calculate below correctly in practice
            '55FF060010000B8802030104010108468F3638DD0E': b'\x88',
            '55ff060010000b8802030104010108468f3abe4346': b'\x88',
            '55ff060011000b1002030104010108468f3c3c89b5': b'\x10',
            '55ff060011000b1002030104010108468f393a07ae': b'\x10'
        }

        # Address 1 Tests:
        for hexCommand in test_data:
            # Assert that the key passed to _headerCheckByte results in the
            # corresponding test_data value:
            self.assertEqual(self.test_pm3_address1._headerCheckByte(unhexlify(hexCommand)[0:7]), test_data[hexCommand], msg='{0}'.format(hexCommand))
            # Assert that the check byte length is equal to one:
            self.assertTrue(len(self.test_pm3_address1._headerCheckByte(unhexlify(hexCommand)[0:7])) == 1, msg='{0}'.format(hexCommand))
            # Assert that the result is an instance of type 'bytes'
            self.assertIsInstance(self.test_pm3_address1._headerCheckByte(unhexlify(hexCommand)[0:7]), bytes, msg='{0}'.format(hexCommand))

    def test_buildReadRequest(self):
        '''
        Tests that read requests are built properly based on the input dataParam

        _buildReadRequest is also dependent on _headerCheckByte and _dataCheckByte
        '''
        test_data = [
            # Test of form (dataParam, address, request)
            ('4001', 1, '55ff0510000006e8010301040101e399'),
            ('4002', 1, '55ff0510000006e80103010402018bb3'),
            ('7001', 1, '55ff0510000006e80103010701018776'),
            ('4001', 2, '55ff051100000661010301040101e399'),
            ('4002', 2, '55ff0511000006610103010402018bb3'),
            ('7001', 2, '55ff0511000006610103010701018776')
        ]

        for test in test_data:
            result = self.assertEqual(PM3(serial=None, address=test[1])._buildReadRequest(dataParam=test[0]), unhexlify(test[2]), \
                                      msg='dataParam: {0}, adr: {1}, cmd: {2}'.format(test[0], test[1], test[2]))

    def test_buildSetTempRequest(self):
        '''
        Tests that set temperature requests are built properly based on the
        input dataParam

        _buildSetTempRequest is also dependent on _headerCheckByte and _dataCheckByte
        '''
        test_data = [
            # Test of form (temperature, address, request)
            (81, 1, '55ff051000000aec01040701010842a20000c4b8'),
            (80, 1, '55ff051000000aec01040701010842a000007c0d'),
            (78, 1, '55ff051000000aec010407010108429c0000712e'),
            (78.5, 1, '55ff051000000aec010407010108429d0000ad74')
        ]

        for test in test_data:
            result = self.assertEqual(PM3(serial=None, address=test[1])._buildSetTempRequest(value=test[0]), unhexlify(test[2]), \
                                      msg='val: {0}, adr: {1}, cmd: {2}'.format(test[0], test[1], test[2]))

    def test_c_to_f(self):
        '''
        Tests C to F temperature conversion
        '''
        test_data = [
            (32, 89.6),
            (0, 32),
            (-9.8765, 14.2223),
            (-45, -49)
        ]

        for test in test_data:
            result = self.assertAlmostEqual(self.test_pm3_address1._c_to_f(test[0]), test[1], \
                                            places=1, msg='c: {0}, f: {1}'.format(test[0], test[1]))

    def test_f_to_c(self):
        '''
        Tests F to C temperature conversion
        '''
        test_data = [
            (89.6, 32),
            (30, -1.1111),
            (-1.23, -18.4611),
            (45, 7.22)
        ]

        for test in test_data:
            result = self.assertAlmostEqual(self.test_pm3_address1._f_to_c(test[0]), test[1], \
                                            places=1, msg='f: {0}, c: {1}'.format(test[0], test[1]))

    def test_validateResponse(self):
        '''
        Tests that the correct boolean is returned for each valid/invalid
        response
        '''
        tests = [
            # Actual Responses Received
            # Tests in the for: (response, address, returned boolean)
            ('55FF060010000B8802030104010108468F3638DD0E', 1, True),
            ('55ff060010000b8802030104010108468f3abe4346', 1, True),
            ('55FF060010000B8802030104010108468F3638DD0E', 1, True),
            ('55ff060010000b8802030104010108468f3abe4346', 1, True),
            ('55ff060011000b1002030104010108468f3c3c89b5', 1, False), # Wrong address
            ('55ff060011000b1002030104010108468f393a07ae', 1, False), # Wrong address
            ('55ff060010000b8802030104010108468f3abe4356', 1, False), # Incorrect dataChk
            ('55FF060010000B8902030104010108468F3638DD0E', 1, False), # Incorrect headerChk
            ('55FF060010000B8802030104010108468F3638DD0E', 2, False), # Wrong address
            ('55ff060010000b8802030104010108468f3abe4346', 2, False), # Wrong address
            ('55FF060010000B8802030104010108468F3638DD0E', 2, False), # Wrong address
            ('55ff060010000b8802030104010108468f3abe4346', 2, False), # Wrong address
            ('55ff060011000b1002030104010108468f3c3c89b5', 2, True),
            ('55ff060011000b1002030104010108468f393a07ae', 2, True),
            ('55ff060010000b8802030104010108468f3abe4356', 2, False), # Incorrect dataChk
            ('55FF060010000B8902030104010108468F3638DD0E', 2, False) # Incorrect headerChk
        ]

        for test in tests:
            result = self.assertIs(PM3(serial=None, address=test[1])._validateResponse(unhexlify(test[0])), \
                                     test[2], msg=test)

# These are all confirmed working requests or responses that can be used to test
# Need some from other addresses and the 'set temp' parameter

# Test check sums:
# 55ff0510000006e8010301040101e399 header should be: b'\xe8', data: b'\xe3\x99'
# 55ff051100000661010301040101e399 header should be: b'\x61', data: b'\xe3\x99'
# 55FF060010000B8802030104010108468F3638DD0E header should be: b'\x88', data: b'\xdd\x0e'
# 55ff060010000b8802030104010108468f3abe4346 header should be: b'\x88', data: b'\x43\x46'
# test that the length of the check byte returns are correct (2 for data, 1 for header)
# test for bytearray type on return

# test _validateResponse for '06' in hexCommand

# test entire write pipeline?? it's basically just _buildRequest...
# test entire read pipeline (i.e. from example responses to output dicts, one assert for each watlow function)

# Need to use variations of the above or similar hex to test valid responses

unittest.main()
