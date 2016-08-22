python-pppd
###########
Simple library for controlling PPP connections with pppd. Under the hood it uses
the `subprocess` module to interact with `pppd` to create and disconnect PPP
connections. Positional and keyword arguments are passed to the `pppd` command-
line although there is protection for shell exploits.

This library has been production tested connecting daily to 280+ remote
locations via dial-up PPP connection for over a year. I have simply packaged and
cleaned up the module as some may find it useful.

Anyone wanting to do something similar in a Windows environment should probably
take a look at `win32ras`.

Requirements
============
You will require `pppd`, the PPP daemon and PPP kernel modules.

Installation
============
To install simply:

    pip install python-pppd

Alternatively, install from the repository:

  git clone https://github.com/cour4g3/python-pppd
  cd python-pppd
  python setup.py install

Getting Started
===============
You can connect to an existing configured PPP connection:

.. code:: python

   >>> from pppd import PPPConnection
   >>> ppp = PPPConnection(call='work') # blocks until connected
   >>> ppp.connected() # check if connected, raises error if connection error
   True
   >>> ppp.laddr # address of local host
   '10.0.0.1'
   >>> ppp.raddr # address of remote client
   '10.0.0.2'

You can specify any positional or keyword arguments:

.. code:: python

   PPPConnection('/dev/ttyS0', connect='/usr/bin/chat -v -f /etc/chatscripts/A1')

Which is equivalent to the following:

    sudo pppd /dev/ttyS0 connect "/usr/bin/chat -v -f /etc/chatscripts/A1"

Normally you require `sudo` to use `pppd`, if you don't have it and have setup
the `pppd` binary with setuid-root or are running as root you can use:

.. code:: python

   PPPConnection(sudo=False)

You can also specify an alternate paths to `pppd` or `sudo` if the libary cannot
find them:

.. code:: python

   PPPConnection(sudo_path='/usr/local/bin/sudo', pppd_path='/usr/local/sbin/pppd')

License
=======
Distributed under the MIT license.
