
from binascii import unhexlify

import pytest

from pywatlow.cli import main
from pywatlow.watlow import Watlow


def test_main():
    main([]) == 0


def test_watlow():
    watlow = Watlow()
    assert watlow.address == 1


class TestWatlow:
    '''
    Test suite for the Watlow class
    * Each command was varified with a response from Watlow device
    * Each response was a real response from a Watlow device
    '''

    def test_dataCheckByte(self):
        '''
        Test that the correct check byte is calculated from the data portion
        of the hex command

        _dataCheckByte is the only function scored in this test
        '''
        test_watlow_address1 = Watlow(serial=None)
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
            dataCheckByte = test_watlow_address1._dataCheckByte(unhexlify(hexCommand)[8:-2])
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
        test_watlow_address1 = Watlow(serial=None)
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
            headerCheckByte = test_watlow_address1._headerCheckByte(unhexlify(hexCommand)[0:7])
            assert headerCheckByte == test_data[hexCommand]
            # Assert that the check byte length is equal to one:
            assert len(headerCheckByte) == 1, hexCommand
            # Assert that the result is an instance of type 'bytes'
            assert isinstance(headerCheckByte, bytes), hexCommand

    def test_buildReadRequest(self):
        '''
        Tests that read requests are built properly based on the input dataParam

        _buildReadRequest is also dependent on _headerCheckByte, _dataCheckByte,
        and _intDataParamToHex
        '''
        test_data = [
            # Test of form (dataParam, address, request)
            ('4001', 1, '55ff0510000006e8010301040101e399'), # Process Value
            ('4002', 1, '55ff0510000006e80103010402018bb3'), # Set point
            ('7001', 1, '55ff0510000006e80103010701018776'),
            ('4001', 2, '55ff051100000661010301040101e399'),
            ('4002', 2, '55ff0511000006610103010402018bb3'),
            ('7001', 2, '55ff0511000006610103010701018776'),
            (4001, 2, '55ff051100000661010301040101e399'),
            (4002, 2, '55ff0511000006610103010402018bb3'),
            (7001, 2, '55ff0511000006610103010701018776'),
            (4005, 1, '55FF0510000006E801030104050183FE'), # Sensor Type
            (4007, 1, '55FF0510000006E801030104070133CD'), # RTD Leads
            (4042, 1, '55FF0510000006E8010301042A01785E'), # Units
            (4015, 1, '55FF0510000006E8010301040F01F303'), # Scale Low
            (4016, 1, '55FF0510000006E8010301041001AA15'), # Scale High
            (4017, 1, '55FF0510000006E8010301041101720C'), # Range Low
            (4018, 1, '55FF0510000006E80103010412011A26'), # Range High
            (4030, 1, '55FF0510000006E8010301041E01BA8F'), # Process error enable
            (4031, 1, '55FF0510000006E8010301041F016296'), # Process error low value
            (4037, 1, '55FF0510000006E8010301042501B0DD'), # Resistance Range of thermistor
            (4014, 1, '55FF0510000006E8010301040E012B1A'), # Filter
            (4028, 1, '55FF0510000006E8010301041C010ABC'), # Input Error Latching
            (4020, 1, '55FF0510000006E8010301041401CA72'), # Display precision
            (4012, 1, '55FF0510000006E8010301040C019B29'), # Calibration offset
            (34005, 1, '55FF0510000006E8010301220501612B'), # Linearization function
            (34029, 1, '55FF0510000006E8010301221D013070'), # Linearization Units
            (34008, 1, '55FF0510000006E8010301220801199B'), # Linearization input point 1
            (34018, 1, '55FF0510000006E8010301221201F8F3'), # Linearization output point 1
            (26021, 1, '55FF0510000006E80103011A15019CFE'), # Process Value function
            (26028, 1, '55FF0510000006E80103011A1C018429'), # Process Value Pressure Units
            (26029, 1, '55FF0510000006E80103011A1D015C30'), # Altitude Units
            (26030, 1, '55FF0510000006E80103011A1E01341A'), # Barometric Pressure
            (26026, 1, '55FF0510000006E80103011A1A01547D'), # Filter
            (8003, 1, '55FF0510000006E8010301080301F00F'), # Heat Algorithm
            (6001, 1, '55FF0510000006E80103010601015B2C'), # Digital I/O Direction
        ]

        for test in test_data:
            readRequest = Watlow(serial=None, address=test[1])._buildReadRequest(dataParam=test[0])
            assert readRequest == unhexlify(test[2]), "param: {0}, addr: {1}, request: {2}".format(*test)

    def test_intDataParamToHex(self):
        '''
        Tests that the integer representing the data parameters are formatted
        to hexidecimal properly for the assembled messages.
        '''
        test_data = [
            # Test of form: dataParam, two byte hex representation
            (4005, '0405'),
            (4007, '0407'),
            (4001, '0401'),
            (7001, '0701'),
            (8003, '0803'),
            (26029, '1a1d'),
            (26026, '1a1a'),
            (26030, '1a1e')
        ]

        for test in test_data:
            generatedDataParam = Watlow()._intDataParamToHex(test[0])
            assert generatedDataParam == test[1]

    def test_byteDataParamToInt(self):
        test_data = [
            (b'\x04\x05', 4005),
            (b'\x04\x07', 4007),
            (b'\x07\x01', 7001),
            (b'\x04*', 4042),
            (b'\x04\x0f', 4015),
            (b'\x04\x10', 4016),
            (b'\x04\x11', 4017),
            (b'\x04\x12', 4018),
            (b'\x04\x1e', 4030),
            (b'\x04\x1f', 4031),
            (b'\x04%', 4037),
            (b'\x04\x0e', 4014),
            (b'\x04\x1c', 4028),
            (b'\x04\x14', 4020),
            (b'\x04\x0c', 4012),
            (b'\x04\x01', 4001),
            (b'\x04\x02', 4002),
            (b'"\x05', 34005),
            (b'"\x1d', 34029),
            (b'"\x08', 34008),
            (b'"\x12', 34018),
            (b'\x1a\x15', 26021),
            (b'\x1a\x1c', 26028),
            (b'\x1a\x1d', 26029),
            (b'\x1a\x1e', 26030),
            (b'\x1a\x1a', 26026),
            (b'\x06\x01', 6001),
            (b'\x08\x03', 8003),
        ]

        for test in test_data:
            generatedDataParam = Watlow()._byteDataParamToInt(test[0])
            assert generatedDataParam == test[1]

    def test_buildWriteRequest(self):
        '''
        Tests that set requests are built properly based on the input dataParam

        _buildWriteRequest is also dependent on _headerCheckByte, _dataCheckByte
        and _intDataParamToHex

        If the type of data is not provided, _buildWriteRequest() also relies on
        read() and _parseResponse() to determine the data value type from a
        read request
        '''
        test_data = [
            # Test of form: dataParam, temperature, value type, address, request
            (7001, 81, float, 1, '55ff051000000aec01040701010842a20000c4b8'),
            ('7001', 81, float, 1, '55ff051000000aec01040701010842a20000c4b8'),
            (7001, 80, float, 1, '55ff051000000aec01040701010842a000007c0d'),
            (7001, 78, float, 1, '55ff051000000aec010407010108429c0000712e'),
            (7001, 78.5, float, 1, '55ff051000000aec010407010108429d0000ad74'),
            (7001, 80, float, 2, '55FF051100000A6501040701010842A000007C0D'),
            (8003, 71, int, 1, '55FF05100300094601040803010F0100478FED'),
            ('8003', 71, int, 1, '55FF05100300094601040803010F0100478FED'),
            (8003, 62, int, 1, '55FF05100300094601040803010F01003EC903'),
            (8003, 71, int, 2, '55FF0511030009CF01040803010F0100478FED'),
            (4005, 95, int, 2, '55FF0511030009CF01040405010F01005F26D8'), # Sensor Type
            (4007, 1, int, 2, '55FF0511030009CF01040407010F0100018B6B'), # RTD Leads
            (4042, 75, int, 2, '55FF0511030009CF0104042A010F01004B6A36'), # Units
            (4015, 0.0, float, 2, '55FF051100000A650104040F0108000000009B21'), # Scale Low
            (4016, 20.0, float, 2, '55FF051100000A6501040410010841A000007D88'), # Scale High
            (4017, 0.0, float, 2, '55FF051100000A65010404110108000000007312'), # Range Low
            (4018, 9999.0, float, 2, '55FF051100000A65010404120108461C3C0004D8'), # Range High
            (4030, 62, int, 2, '55FF0511030009CF0104041E010F01003E3CC5'), # Process error enable
            (4031, 0.0, float, 2, '55FF051100000A650104041F0108000000005294'), # Process error low value
            (4037, 1449, int, 2, '55FF0511030009CF01040425010F0105A947B1'), # Resistance Range of thermistor
            (4014, 0.5, float, 2, '55FF051100000A650104040E01083F0000004540'), # Filter
            (4028, 62, int, 2, '55FF0511030009CF0104041C010F01003E6ACD'), # Input Error Latching
            (4020, 105, int, 2, '55FF0511030009CF01040414010F01006908CA'), # Display precision
            (4012, 0.0, float, 2, '55FF051100000A650104040C010800000000F589'), # Calibration offset
            (34005, 62, int, 2, '55FF0511030009CF01042205010F01003EE791'), # Linearization function
            (34029, 1539, int, 2, '55FF0511030009CF0104221D010F010603B94C'), # Linearization Units
            (34008, 0.0, float, 2, '55FF051100000A6501042208010800000000C24D'), # Linearization input point 1
            (34018, 0.0, float, 2, '55FF051100000A65010422120108000000005C11'), # Linearization output point 1
            (26021, 62, int, 2, '55FF0511030009CF01041A15010F01003EF1DB'), # Process Value function
            (26028, 1671, int, 2, '55FF0511030009CF01041A1C010F0106871882'), # Process Value Pressure Units
            (26029, 1677, int, 2, '55FF0511030009CF01041A1D010F01068D6929'), # Altitude Units
            (26030, 14.7, float, 2, '55FF051100000A6501041A1E0108416B3333C7D9'), # Barometric Pressure
            (26026, 0.0, float, 2, '55FF051100000A6501041A1A010800000000840F'), # Filter
            (6001, 68, int, 2, '55FF0511030009CF01040601010F0100446351'), # Digital I/O Direction
        ]

        for test in test_data:
            writeRequest = Watlow(serial=None, address=test[3])._buildWriteRequest(dataParam=test[0], value=test[1], val_type=test[2])
            assert writeRequest == unhexlify(test[4]), "param: {0}, val: {1}, type: {2}, addr: {3}, request: {4}".format(*test)

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
            convertedTemp = Watlow(serial=None)._c_to_f(test[0])
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
            convertedTemp = Watlow(serial=None)._f_to_c(test[0])
            assert convertedTemp == pytest.approx(test[1])

    def test_validateResponse(self):
        '''
        Tests that the correct boolean is returned for each valid/invalid
        response
        '''
        tests = [
            # Actual Responses Received
            # Tests in the form: (response, address, returned boolean)
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
            validateResponse = Watlow(serial=None, address=test[1])._validateResponse(unhexlify(test[0]))
            assert validateResponse == test[2], 'msg: {0}, addr: {1}, bool: {2}'.format(*test)

    def test_parseResponse(self):
        '''
        Tests that the correct data, param, address, and error is being extracted
        from each type of response

        Also dependent on _validateResponse
        '''

        tests = [
            # Actual responses received
            # Tests in the form: (response, param, address, data, error)
            ('55FF06031100097702040803010F010047883B', 8003, 2, 71, False),
            ('55FF06031100097702040803010F010047883B', None, 1, None, True), # Param: 8003, error from wrong address
            ('55FF060011000AEE02040701010842A000001579', 7001, 2, 80.0, False),
            ('55FF060011000B1002030104010108451E40B2F377', 4001, 2, 2532.04345703125, False),
            ('55FF0600110002170280FFB8', None, 2, None, True) # Param: 4001, error from trying to write to read-only param
        ]

        for test in tests:
            generatedOutput = Watlow(serial=None, address=test[2])._parseResponse(unhexlify(test[0]))
            test_msg = 'msg: {0}, param: {1}, addr: {2}, data: {3}, isError: {4}'.format(*test)
            assert generatedOutput['data'] == test[3], test_msg
            assert generatedOutput['param'] == test[1], test_msg
            assert generatedOutput['address'] == test[2], test_msg
            assert (type(generatedOutput['error']) is Exception) == test[4], test_msg
