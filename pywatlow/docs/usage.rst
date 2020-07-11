=====
Usage
=====

Command Line Usage
==================

Format::

	pywatlow [-h] [-r PORT ADDR PARAM | -s PORT ADDR TEMP]

Read the current temperature in degrees Celsius.
This is equivalent to calling `Watlow(port='COM5',address=1).readParam(4001)`::

	# Read the current temperature (parameter 4001) of the Watlow controller
	# at address 1 (Watlow controller's default) on serial port COM5:
	>>> pywatlow -r COM5 1 4001
	{'address': 1, 'data': 50.5, 'error': None}

Read the setpoint temperature in degrees Celsius.
This is equivalent to calling `Watlow(port='COM5',address=1).readParam(7001)`::

	# Read the setpoint (parameter 7001) of the Watlow controller
	# at address 1 on serial port COM5:
	>>> pywatlow -r COM5 1 7001
	{'address': 1, 'data': 60.0, 'error': None}

Change the setpoint temperature (degrees Celsius).
This is equivalent to calling `Watlow(port='COM5',address=1).setTemp(50)`::

	# Change the setpoint of the Watlow controller
	# at address 1 on serial port COM5:
	>>> pywatlow -s COM5 1 50
	{'address': 1, 'data': 50.0, 'error': None}


Module Usage
============

To use pywatlow in a project::

	from pywatlow.watlow import Watlow
	watlow = Watlow(port='COM5', address=1)
	print(watlow.readParam(4001))
	print(watlow.readParam(7001))
	print(watlow.setTemp(55))

	##### Returns #####
	{'address': 1, 'data': 50.5, 'error': None}
	{'address': 1, 'data': 50.0, 'error': None}
	{'address': 1, 'data': 55.0, 'error': None}

Using multiple temperature controllers on a single USB to RS485 converter::

	from pywatlow.watlow import Watlow
	import serial

	ser = serial.Serial()
	ser.port = 'COM5'
	ser.baudrate = 38400  # Default baudrate for Watlow controllers
	ser.timeout = 0.5
	ser.open()

	watlow_one = Watlow(serial=ser, address=1)
	watlow_two = Watlow(serial=ser, address=2)
	print(watlow_one.readParam(4001))
	print(watlow_two.readParam(4001))

	##### Returns #####
	{'address': 1, 'data': 50.5, 'error': None}
	{'address': 2, 'data': 60.0, 'error': None}


Reading Other Parameters
========================

Currently, only parameters for the current temperature (4001) and the setpoint (7001)
have been tested.


Error Handling
==============

Errors are passed through using the 'error' key of the returned dictionary.
Here there is no temperature controller at address 2::

	print(watlow_one.readParam(4001))
	print(watlow_two.readParam(4001))

	##### Returns #####
	{'address': 1, 'data': 55.0, 'error': None}
	{'address': 2, 'data': None, 'error': Exception('Exception: No response at address 2')}
