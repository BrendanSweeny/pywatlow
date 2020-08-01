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
	{'address': 1, 'param': 4001, 'data': 50.5, 'error': None}

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
	{'address': 1, 'param': 7001, 'data': 60.0, 'error': None}


Module Usage
============

To use pywatlow in a project::

	from pywatlow.watlow import Watlow
	watlow = Watlow(port='COM5', address=1)
	print(watlow.readParam(4001))
	print(watlow.readParam(7001))
	print(watlow.setTemp(55))

	##### Returns #####
	{'address': 1, 'param': 4001, 'data': 50.5, 'error': None}
	{'address': 1, 'param': 7001, 'data': 50.0, 'error': None}
	{'address': 1, 'param': 7001, 'data': 55.0, 'error': None}

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
	{'address': 1, 'param': 4001, 'data': 50.5, 'error': None}
	{'address': 2, 'param': 4001, 'data': 60.0, 'error': None}


Reading Other Parameters
========================

The messaging structure for Watlow temperature controllers is set up to return data
as integers or floats depending on the nature of the data. Often, ints are used
to represent a state, such as in parameter ID 8003, the control loop heat algorithm.
Here, a returned value of 71 corresponds to the PID algorithm, whereas 64 corresponds
to a simpler "on-off" algorithm.

We can read the state of 8003 like so::

	from pywatlow.watlow import Watlow
	watlow = Watlow(port='COM5', address=1)

	watlow.readParam(8003)

	##### Returns #####
	{'address': 1, 'param': 8003, 'data': 71, 'error': None}  # 71 --> PID algorithm

See the Watlow user manual for more information about the different parameter IDs
and their functions.

Setting Other Parameters
========================

`watlow.setParam()` is used to write to specific Watlow parameters.
The message structure required for the set request depends on the data type (int or float).
Pywatlow will build the message based on this data type, which can be specified by
passing the type class (either `int` or `float`) to the `val_type` argument.

`val_type` is optional. If `val_type=None`, pywatlow will first attempt to read the state
of the passed parameter ID in order to determine the correct way to build the
message, then Pywatlow will write the value to the parameter. Passing the incorrect type to
`val_type` will result in an error (e.g. `watlow.setParam(7001, 200.0, int)`).
To see which data type each parameter expects, see the Watlow controller `documentation <https://www.watlow.com/-/media/documents/user-manuals/pm-pid-1.ashx>`_.

Error Handling
==============

Errors are passed through using the 'error' key of the returned dictionary.
Here there is no temperature controller at address 2::

	print(watlow_one.readParam(4001))
	print(watlow_two.readParam(4001))

	##### Returns #####
	{'address': 1, 'param': 4001, 'data': 55.0, 'error': None}
	{'address': 2, 'param': None, 'data': None, 'error': Exception('Exception: No response at address 2')}
