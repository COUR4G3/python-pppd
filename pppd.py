import fcntl
import os
import signal
import re
import time

from subprocess import Popen, PIPE, STDOUT

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

try:
    __version__ = version("python-pppd")
except:
    __version__ = "0.1-dev0"


PPPD_RETURNCODES = {
    1:  'Fatal error occured',
    2:  'Error processing options',
    3:  'Not executed as root or setuid-root',
    4:  'No kernel support, PPP kernel driver not loaded',
    5:  'Received SIGINT, SIGTERM or SIGHUP',
    6:  'Modem could not be locked',
    7:  'Modem could not be opened',
    8:  'Connect script failed',
    9:  'pty argument command could not be run',
    10: 'PPP negotiation failed',
    11: 'Peer failed (or refused) to authenticate',
    12: 'The link was terminated because it was idle',
    13: 'The link was terminated because the connection time limit was reached',
    14: 'Callback negotiated',
    15: 'The link was terminated because the peer was not responding to echo reque               sts',
    16: 'The link was terminated by the modem hanging up',
    17: 'PPP negotiation failed because serial loopback was detected',
    18: 'Init script failed',
    19: 'Failed to authenticate to the peer',
}

class PPPConnectionError(Exception):
    def __init__(self, code, output=None):
        self.code = code
        self.message = PPPD_RETURNCODES.get(code, 'Undocumented error occured')
        self.output = output

        super(Exception, self).__init__(code, output)

    def __str__(self):
        return self.message

class PPPConnection:
    def __init__(self, *args, **kwargs):
        self.output = b''
        self._laddr = None
        self._raddr = None

        commands = []

        if kwargs.pop('sudo', True):
            sudo_path = kwargs.pop('sudo_path', '/usr/bin/sudo')
            if not os.path.isfile(sudo_path) or not os.access(sudo_path, os.X_OK):
                raise IOError('%s not found' % sudo_path)
            commands.append(sudo_path)

        pppd_path = kwargs.pop('pppd_path', '/usr/sbin/pppd')
        if not os.path.isfile(pppd_path) or not os.access(pppd_path, os.X_OK):
            raise IOError('%s not found' % pppd_path)

        commands.append(pppd_path)

        for k,v in kwargs.items():
            commands.append(k)
            commands.append(v)
        commands.extend(args)
        commands.append('nodetach')
        commands.append('debug')

        self.proc = Popen(commands, 
            stdout=PIPE, 
            stderr=STDOUT, 
            preexec_fn=os.setsid)
        
        # set stdout to non-blocking
        fd = self.proc.stdout.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

        while True:
            try:
                data = self.proc.stdout.read()
                if data:
                    self.output += data
            except IOError as e:
                if e.errno != 11:
                    raise
                time.sleep(1)
            if b'ip-up finished' in self.output:
                return
            elif self.proc.poll():
                raise PPPConnectionError(self.proc.returncode, self.output)

    @property
    def laddr(self):
        if not self._laddr:
            try:
                data = self.proc.stdout.read()
                if data:
                    self.output += data
            except IOError as e:
                if e.errno != 11:
                    raise
            result = re.search(rb'local  IP address ([\d\.]+)', self.output)
            if result:
                self._laddr = result.group(1)

        return self._laddr

    @property
    def raddr(self):
        if not self._raddr:
            try:
                data = self.proc.stdout.read()
                if data:
                    self.output += data
            except IOError as e:
                if e.errno != 11:
                    raise
            result = re.search(rb'remote IP address ([\d\.]+)', self.output)
            if result:
                self._raddr = result.group(1)

        return self._raddr

    def connected(self):
        if self.proc.poll():
            try:
                data = self.proc.stdout.read()
                if data:
                    self.output += data
            except IOError as e:
                if e.errno != 11:
                    raise
            if self.proc.returncode not in [0, 5]:
                raise PPPConnectionError(self.proc.returncode, self.output)
            return False
        elif b'ip-up finished' in self.output:
            return True

        return False

    def disconnect(self):
        try:
            if not self.connected():
                return
        except PPPConnectionError:
            return

        # Send the signal to all the processes in group
        # Based on stackoverlfow: 
        # https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true/
        os.killpg(os.getpgid(self.proc.pid), signal.SIGHUP)
        os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)

