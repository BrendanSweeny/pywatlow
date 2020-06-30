
from binascii import unhexlify

import pytest

from pywatlow.cli import main
from pywatlow.PM3 import PM3


def test_main():
    assert main([]) == 0


def test_PM3():
    pm3 = PM3()
    assert pm3.address == 1


class TestPM3:
    '''
    Test suite for the PM3 class
    * Each command was varified with a response from Watlow PM3
    * Each response was a real response from a Watlow PM3
    '''

    def test_dataCheckByte(self):
        '''
        Test that the correct check byte is calculated from the data portion
        of the hex command

        _dataCheckByte is the only function scored in this test
        '''
        test_pm3_address1 = PM3(serial=None)
        test_data = {
            # Request, Address 1, '4001'
            '55ff0510000006e8010301040101e399': b'\xe3\x99',
            # Request, Address 2, '4001'
            '55ff051100000661010301040101e399': b'\xe3\x99',
            # Request, Address 2, '7001'
            '55ff0511000006610103010701018776': b'\x87\x76',
            # Responses (not necessarily from requests above)
            '55FF060010000B8802030104010108468F3638DD0E': b'\xdd\x0e',
            '55ff060010000b8802030104010108468f3abe4346': b'\x43\x46',
            '55ff060011000b1002030104010108468f393a07ae': b'\x07\xae',
            '55ff060011000b100203010701010842960000d3b0': b'\xd3\xb0'
        }

        for hexCommand in test_data:
            # Assert that the key passed to _dataCheckByte results in the
            # corresponding test_data value:
            dataCheckByte = test_pm3_address1._dataCheckByte(unhexlify(hexCommand)[8:-2])
            assert dataCheckByte == test_data[hexCommand], hexCommand
            # Assert that the check byte length is equal to two:
            assert len(dataCheckByte) == 2, hexCommand
            # Assert that the result is an instance of type 'bytes'
            assert isinstance(dataCheckByte, bytes), hexCommand

    def test_headerCheckByte(self):
        '''
        Tests that the correct check byte is calculated from the header
        portion of the hex command

        Watlow zone/address is the only parameter changed in the header by users

        _headerCheckByte is the only function scored by this test
        '''
        test_pm3_address1 = PM3(serial=None)
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
            headerCheckByte = test_pm3_address1._headerCheckByte(unhexlify(hexCommand)[0:7])
            assert headerCheckByte == test_data[hexCommand]
            # Assert that the check byte length is equal to one:
            assert len(headerCheckByte) == 1, hexCommand
            # Assert that the result is an instance of type 'bytes'
            assert isinstance(headerCheckByte, bytes), hexCommand

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
            readRequest = PM3(serial=None, address=test[1])._buildReadRequest(dataParam=test[0])
            assert readRequest == unhexlify(test[2]), "param: {0}, addr: {1}, request: {2}".format(*test)

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
            setTempRequest = PM3(serial=None, address=test[1])._buildSetTempRequest(value=test[0])
            assert setTempRequest == unhexlify(test[2]), "param: {0}, addr: {1}, request: {2}".format(*test)

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
            convertedTemp = PM3(serial=None)._c_to_f(test[0])
            assert convertedTemp == pytest.approx(test[1])

    def test_f_to_c(self):
        '''
        Tests F to C temperature conversion
        '''
        test_data = [
            (89.6, 32),
            (30, -1.1111111111),
            (-1.23, -18.4611),
            (45, 7.2222222222)
        ]

        for test in test_data:
            convertedTemp = PM3(serial=None)._f_to_c(test[0])
            assert convertedTemp == pytest.approx(test[1])

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
            ('55ff060011000b1002030104010108468f3c3c89b5', 1, False),  # Wrong address
            ('55ff060011000b1002030104010108468f393a07ae', 1, False),  # Wrong address
            ('55ff060010000b8802030104010108468f3abe4356', 1, False),  # Incorrect dataChk
            ('55FF060010000B8902030104010108468F3638DD0E', 1, False),  # Incorrect headerChk
            ('55FF060010000B8802030104010108468F3638DD0E', 2, False),  # Wrong address
            ('55ff060010000b8802030104010108468f3abe4346', 2, False),  # Wrong address
            ('55FF060010000B8802030104010108468F3638DD0E', 2, False),  # Wrong address
            ('55ff060010000b8802030104010108468f3abe4346', 2, False),  # Wrong address
            ('55ff060011000b1002030104010108468f3c3c89b5', 2, True),
            ('55ff060011000b1002030104010108468f393a07ae', 2, True),
            ('55ff060010000b8802030104010108468f3abe4356', 2, False),  # Incorrect dataChk
            ('55FF060010000B8902030104010108468F3638DD0E', 2, False)  # Incorrect headerChk
        ]

        for test in tests:
            validateResponse = PM3(serial=None, address=test[1])._validateResponse(unhexlify(test[0]))
            assert validateResponse == test[2], 'msg: {0}, addr: {1}, bool: {2}'.format(*test)
