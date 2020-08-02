Watlow Messaging Structure
==========================

The following is an incomplete understanding of the messaging structure that
the Watlow temperature controllers use. Enough of the structure is understood
for the driver to be functional, but the function of many of the bytes is unknown
to the author(s).

General Message Structure:

* BACnet MS/TP protocol
* First two bytes of any message make up the preamble, and are always: 55 FF
* Byte 3 seems to define the type of message (read/response)
* Byte 4 of the request defines the zone (internal Watlow address)
* The zone appears in byte 5 of the response
* Byte 7 appears to define the type of request
* Byte 8 is the header check byte (more info at `reverseengineering.stackexchange.com <https://reverseengineering.stackexchange.com/questions/8303/rs-485-checksum-reverse-engineering-watlow-ez-zone-pm>`_)
* Immediately following the parameter bytes is the instance. I have yet to encounter a situation where this is not 01
* The final two bytes of any message are the data check bytes (more info at `reverseengineering.stackexchange.com <https://reverseengineering.stackexchange.com/questions/8303/rs-485-checksum-reverse-engineering-watlow-ez-zone-pm>`_)


How to read the example message tables:

* Addr.: The address used in the request and response
* Param: The parameter being read/set
* Process Val.: The value represented in the "Data" column of the response/request
* The message begins with the column labeled "Preamble" and continues to the right
* Sometimes the byte number is not the same in the response as the request (e.g. Zone), hence the "-"

Read Requests
-------------

* Read requests seem to be 16 bytes long no matter the data type
* Byte 7 is 06 for read requests
* Bytes 12 and 13 represent the parameter to be read
* Byte 14 is the instance, generally 01

Where the response is a float:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Request is 16 bytes long
* Response is 21 bytes long
* Response types appear to be defined by bytes 7
* Note: The process value for 4001 is ~2500 in these examples because no probe is connected

.. csv-table:: Example Messages
  :file: messages_read_float.csv
  :header-rows: 1

Where the response is an integer:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Request is 16 bytes long
* Response is 20 bytes long

.. csv-table:: Example Messages
  :file: messages_read_int.csv
  :header-rows: 1

Set Requests
------------

* Bytes 11 and 12 represent the parameter to be set
* Byte 13 is the instance, generally 01

Where the value/response is a float
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Request is 20 bytes long
* Response is 20 bytes long
* Byte 7 is 0A when the process value is a float
* When the process value is a float, the byte preceding the data (14) is 08

.. csv-table:: Example Messages
  :file: messages_set_float.csv
  :header-rows: 1

Where the value/response is an integer:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Request is 19 bytes long
* Response is 19 bytes long
* Byte 7 is 09 when the process value is an integer
* When the process value is an integer, the two bytes preceeding the data (14, 15) are 0F 01

.. csv-table:: Example Messages
  :file: messages_set_int.csv
  :header-rows: 1

Errors
^^^^^^

Currently, it is unclear exactly what these responses mean, or what the structure of an error message is, but the following are possibly errors:

This is likely an access denied error response received when trying to write a
read only parameter (4001, 100 degrees, address 2):

* `55 FF 06 00 11 00 02 17 02 80 FF B8`

Other possible errors that have been received:

* `55 FF 06 00 10 00 02 8F 02 85 52 EF`
* `55 FF 06 00 10 00 02 8F 02 86 C9 DD`
* `55 FF 06 00 10 00 02 8F 02 83 64 8A`
* `55 FF 06 00 10 00 02 8F 02 80 FF B8`
* `55 FF 06 00 10 00 05 73 02 05 08 03 00 02 5B`
* `55 FF 06 00 10 00 05 73 02 05 01 08 00 B4 23`
