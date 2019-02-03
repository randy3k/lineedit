from .vt100_console import Vt100Console
import array
import fcntl
import termios


class PosixConsole(Vt100Console):
    def get_size(self):
        buf = array.array('h', [0, 0, 0, 0])
        fcntl.ioctl(self.fileno(), termios.TIOCGWINSZ, buf)

        return buf[0], buf[1]
