========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/pywatlow/badge/?style=flat
    :target: https://readthedocs.org/projects/pywatlow
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/BrendanSweeny/pywatlow.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/BrendanSweeny/pywatlow

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/BrendanSweeny/pywatlow?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/BrendanSweeny/pywatlow

.. |requires| image:: https://requires.io/github/BrendanSweeny/pywatlow/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/BrendanSweeny/pywatlow/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/BrendanSweeny/pywatlow/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/BrendanSweeny/pywatlow

.. |version| image:: https://img.shields.io/pypi/v/pywatlow.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/pywatlow

.. |wheel| image:: https://img.shields.io/pypi/wheel/pywatlow.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/pywatlow

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pywatlow.svg
    :alt: Supported versions
    :target: https://pypi.org/project/pywatlow

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pywatlow.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/pywatlow

.. |commits-since| image:: https://img.shields.io/github/commits-since/BrendanSweeny/pywatlow/v0.1.2.svg
    :alt: Commits since latest release
    :target: https://github.com/BrendanSweeny/pywatlow/compare/v0.1.2...master



.. end-badges

A Python 3 driver for the Watlow EZ-Zone PM temperature controller standard bus protocol.
This driver allows the user to access each of the parameters outlined in the Watlow
`user manual <https://www.watlow.com/-/media/documents/user-manuals/pm-pid-1.ashx>`_
with just a few functions.

* Free software: GNU Lesser General Public License v3 (LGPLv3)

Installation
============

::

    pip install pywatlow

You can also install the in-development version with::

    pip install https://github.com/BrendanSweeny/pywatlow/archive/master.zip


Documentation
=============


https://pywatlow.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
