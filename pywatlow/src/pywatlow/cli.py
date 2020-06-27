"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mpywatlow` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``pywatlow.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``pywatlow.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import sys
import argparse
from pywatlow.PM3 import PM3

parser = argparse.ArgumentParser(description='A Python driver for Watlow temperature controllers')
group = parser.add_mutually_exclusive_group()
group.add_argument('-r', '--read', metavar=('PORT', 'ADDR', 'PARAM'), nargs=3,
                    help='Read a specific Watlow parameter. Specify the port, RS485 address, and parameter to read (e.g. "4001" for temperature, "7001" for setpoint). Other values can be found in the Watlow user manual')
group.add_argument('-s', '--set', metavar=('PORT', 'ADDR', 'TEMP'), nargs=3,
                    help='Change the setpoint temperature. Specify the port, RS485 address, and desired setpoint temperature in Celcius')


def main(args=None):
    """
    Example usage:
    pywatlow COM5 1 set 100
    """
    args = parser.parse_args(args=args)

    if args.read:
        pm3 = PM3(port=args.read[0], address=int(args.read[1]))
        print(pm3.readParam(int(args.read[2])))
    elif args.set:
        pm3 = PM3(port=args.set[0], address=int(args.set[1]))
        print(pm3.setTemp(int(args.set[2])))
    return 0
