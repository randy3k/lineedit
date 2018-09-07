from __future__ import unicode_literals

import os
import select

import tty
import termios

from codecs import getincrementaldecoder
from .key import KeyEvent
from .vt100_parser import Vt100Parser


class PosixReader:
    """
    Make reading stdin non blocking
    """
    def __init__(self, stdin):
        self.fd = stdin.fileno()
        # make sure decoding is continuous
        decoder_cls = getincrementaldecoder('utf-8')
        self.decoder = decoder_cls("surrogateescape")

    def fileno(self):
        return self.fd

    def read(self, count=1024):
        if not select.select([self.fd], [], [], 0)[0]:
            return ""

        data = os.read(self.fd, count)
        return self.decoder.decode(data)


class PosixStream:

    def __init__(self, stdin):
        self.stdin = PosixReader(stdin)
        self._parser = Vt100Parser(callback=self._append_key_event)

    def wait_until_ready(self, timeout=None):
        rlist = [self.stdin.fileno()]
        return select.select(rlist, [], [], timeout)[0]

    def read(self):
        data = self.stdin.read()
        self._key_events = []
        self._parser.feed(data)
        return self._key_events

    def _append_key_event(self, key, data=None):
        if type(key) is tuple:
            for k in key:
                self._key_events.append(KeyEvent(k, data))
        else:
            self._key_events.append(KeyEvent(key, data))

    def raw_mode(self):
        return raw_mode(self.stdin.fileno())

    def cooked_mode(self):
        return cooked_mode(self.stdin.fileno())


class raw_mode(object):
    """
    clone from prompt_toolkit
    """
    def __init__(self, fileno):
        self.fileno = fileno
        try:
            self.attrs_before = termios.tcgetattr(fileno)
        except termios.error:
            self.attrs_before = None

    def __enter__(self):
        try:
            newattr = termios.tcgetattr(self.fileno)
        except termios.error:
            pass
        else:
            newattr[tty.LFLAG] = self._patch_lflag(newattr[tty.LFLAG])
            newattr[tty.IFLAG] = self._patch_iflag(newattr[tty.IFLAG])
            newattr[tty.CC][termios.VMIN] = 1

            termios.tcsetattr(self.fileno, termios.TCSANOW, newattr)
            os.write(self.fileno, b'\x1b[?1l')

    @classmethod
    def _patch_lflag(cls, attrs):
        return attrs & ~(termios.ECHO | termios.ICANON | termios.IEXTEN | termios.ISIG)

    @classmethod
    def _patch_iflag(cls, attrs):
        return attrs & ~(
            termios.IXON | termios.IXOFF |
            termios.ICRNL | termios.INLCR | termios.IGNCR
        )

    def __exit__(self, *a, **kw):
        if self.attrs_before is not None:
            try:
                termios.tcsetattr(self.fileno, termios.TCSANOW, self.attrs_before)
            except termios.error:
                pass


class cooked_mode(raw_mode):
    """
    clone from prompt_toolkit
    """
    @classmethod
    def _patch_lflag(cls, attrs):
        return attrs | (termios.ECHO | termios.ICANON | termios.IEXTEN | termios.ISIG)

    @classmethod
    def _patch_iflag(cls, attrs):
        return attrs | termios.ICRNL
