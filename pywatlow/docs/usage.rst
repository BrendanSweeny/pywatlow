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

Read the setpoint temperature in degress Celsius.
This is equivalent to calling `Watlow(port='COM5',address=1).readParam(7001)`::

	# Read the setpoint (parameter 7001) of the Watlow controller
	# at address 1 on serial port COM5:
	>>> pywatlow -r COM5 1 7001
	{'address': 1, 'data': 50.0, 'error': None}


Module Usage
============

To use pywatlow in a project::

	from pywatlow.watlow import Watlow
	watlow = Watlow()
	watlow.port = 'COM5'
	watlow.open()
	print(watlow.readParam(4001))
	print(watlow.readParam(7001))
	print(watlow.setTemp(55))

Returns::

	>>> {'address': 1, 'data': 50.5, 'error': None}
	>>> {'address': 1, 'data': 50.0, 'error': None}
	>>> {'address': 1, 'data': 55.0, 'error': None}
