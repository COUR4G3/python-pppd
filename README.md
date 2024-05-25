# python-pppd

Simple library for controlling PPP connections with pppd.

Under the hood it uses the `subprocess` module to interact with `pppd` to create and disconnect PPP
connections.


## Installation

Make sure `pppd` is installed on your system, typically on Ubuntu/Debian:

```shell
$ apt-get install pppd
```


And on Fedora/CentOS/RedHat:

```shell
$ dnf install pppd
```


Then you can install the latest release from PyPi:

```shell
$ pip install python-pppd
```


Alternatively, clone and install the latest development version from GitHub:

```shell
$ git clone https://github.com/cour4g3/python-pppd
$ cd python-pppd
$ pip install -e .
```


## Getting Started

You can connect to an existing configured PPP connection:

```python
>>> from pppd import PPPConnection
>>> ppp = PPPConnection(call='work') # blocks until connected
>>> ppp.connected() # check if connected, raises error if connection error
True
>>> ppp.laddr # address of local host
'10.0.0.1'
>>> ppp.raddr # address of remote client
'10.0.0.2'
```


You can specify any positional or keyword arguments:

```python
>>> PPPConnection('/dev/ttyS0', connect='/usr/bin/chat -v -f /etc/chatscripts/A1')
```

Which is equivalent to the following:

```shell
$ sudo pppd /dev/ttyS0 connect "/usr/bin/chat -v -f /etc/chatscripts/A1"
```


Normally you require `sudo` to use `pppd`, if you don't have it and have setup
the `pppd` binary with setuid-root or are running as root you can use:

```python
>>> PPPConnection(sudo=False)
```


You can also specify an alternate paths to `pppd` or `sudo` if the libary cannot
find them:

```python
>>> PPPConnection(sudo_path='/usr/local/bin/sudo', pppd_path='/usr/local/sbin/pppd')
```


License
=======

Licensed under the MIT license.
