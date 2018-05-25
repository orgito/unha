Unha
========
.. image:: https://img.shields.io/pypi/v/unha.svg?style=flat-square
    :target: https://pypi.org/project/unha

.. image:: https://img.shields.io/pypi/pyversions/unha.svg?style=flat-square
    :target: https://pypi.org/project/unha

.. image:: https://img.shields.io/pypi/l/unha.svg?style=flat-square
    :target: https://pypi.org/project/unha

-----

A library to simplify telnet connections to Cisco IOS devices


Installation
------------

Unha is distributed on PyPI and is available on Linux/macOS and Windows and supports Python 3.6+.

.. code-block:: bash

    $ pip install -U unha

Why not just use Netmiko?
-------------------------

I use Netmiko whenever possible. Unfortunately I have some old cisco devices that just refuse to
work with Netmiko. I spent a lot of time trying to make it work but eventually gave up.

Unha is a fallback library that I use when Netmiko with ``cisco_ios_telnet`` fails to connect to my
stuborn devices.

Usually my scripts will try to connect to the devices using the fololwing methods:

- Netmiko with device_type ``cisco_ios``
- Netmiko with device_type ``cisco_ios_telnet``
- Unha


Usage
-----

I try to emulate the Netmiko methods.

.. code-block:: python

    >>> device = Unha('10.0.0.1', 'username', 'password')
    >>> output = device.send_command('show version')
    >>> device.send_config_set(['snmp ifmib ifindex persist', 'snmp-server enable traps cpu threshold'])
    >>> device.disconnect()

