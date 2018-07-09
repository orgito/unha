# pylint: disable=C0111
import re
from telnetlib import Telnet


class UnhaException(Exception):
    pass


class UnhaAuthException(UnhaException):
    pass


def normalize_linefeeds(a_string):
    newline = re.compile('(\r\r\r\n|\r\r\n|\r\n|\n\r)')
    a_string = newline.sub('\n', a_string)
    return re.sub('\r', '\n', a_string)


class Unha(object):

    def __init__(self, host, username, password, timeout=30):
        self.device = None
        self.prompt = ''
        self.host = host
        self.username = username
        self.password = password
        self.timeout = timeout
        self.connect()

    def check_enable_mode(self):
        self.device.write(b'\n')
        (i, obj, res) = self.device.expect([b'#', b'>'], timeout=self.timeout)
        if i == 0:
            return True
        return False

    def connect(self):
        self.device = Telnet(self.host)
        (i, obj, res) = self.device.expect([b'name:', b'ser:', b'ogin:'])
        if i == -1:
            raise UnhaException('Unable to detect login prompt')
        login_prompt = obj.group()
        self.device.write(self.username.encode('ascii') + b'\n')
        self.device.read_until(b'assword:')
        self.device.write(self.password.encode('ascii') + b'\n')
        (i, obj, res) = self.device.expect([b'#', b'>', login_prompt])
        if i == -1:
            raise UnhaAuthException('Authentication failed.')
        if i == 2:
            self.device.close()
            raise UnhaAuthException('Authentication failed.')
        self.prompt = res.strip()
        if i == 0:
            self._send_command('terminal length 0')
            self._send_command('terminal width 511')

    def disconnect(self):
        self.device.close()

    def enable(self):
        if self.check_enable_mode():
            return ''
        self.device.write(b'enable\n')
        self.device.read_until(b'assword:')
        self.device.write(self.password.encode('ascii') + b'\n')
        (i, obj, res) = self.device.expect([b'#', b'assword:'])
        if i == -1:
            raise UnhaAuthException('Enable failed.')
        if i == 1:
            self.device.close()
            raise UnhaAuthException('Enable failed.')
        self.prompt = res.splitlines()[-1].strip()
        print(self.prompt)
        self._send_command('terminal length 0')
        self._send_command('terminal width 511')
        return ''

    def send_command(self, cmd='', prompt=None):
        output = self._send_command(cmd, prompt).splitlines()
        return '\n'.join(output[1:-1])

    def send_config_set(self, config_commands=None):
        if config_commands is None:
            return ''
        if isinstance(config_commands, str):
            config_commands = (config_commands,)
        self._send_command('end')
        output = self._send_config_cmd('config term')
        for line in config_commands:
            output += self._send_config_cmd(line)
        output += self._send_command('end')
        return output

    def _send_command(self, cmd='', prompt=None):
        if prompt is None:
            prompt = self.prompt
        else:
            prompt = prompt.encode('ascii')
        self.device.write(cmd.encode('ascii') + b'\n')
        output = normalize_linefeeds(self.device.read_until(prompt).decode('ascii'))
        return output

    def _send_config_cmd(self, cmd=None):
        if cmd is None:
            return ''
        return self._send_command(cmd, prompt=')#')
