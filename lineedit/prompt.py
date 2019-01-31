import sys
import time
import asyncio

from .buffer import Buffer
from .current import focusing_buffer
from .layout import Layout
from .key_bindings import default_bindings
from .key_processor import KeyProcessor
from .utils import is_windows

from .renderer import Renderer
if is_windows():
    from .win32_stream import Win32Stream
else:
    from .posix_stream import PosixStream
    from .posix_console import PosixConsole


class Prompt:
    def __init__(self, message=''):
        self.buffer = Buffer()
        self.bindings = default_bindings()
        self.processor = KeyProcessor(self.bindings)

        if is_windows():
            self.stream = Win32Stream(sys.stdin)
        else:
            self.stream = PosixStream(sys.stdin)
            self.console = PosixConsole(sys.stdout)

        self.layout = Layout(message, self.buffer)
        self.renderer = Renderer(self.layout, self.console)

    def run(self):

        self.console.enable_bracketed_paste()
        self.console.enable_autowrap()
        self.console.flush()
        self.renderer.render()

        @asyncio.coroutine
        def input_hook():
            while True:
                if self.stream.wait_until_ready(timeout=0):
                    return
                time.sleep(0.03)

        @asyncio.coroutine
        def run_async():
            while True:
                if self.stream.wait_until_ready(timeout=0):
                    data = self.stream.read()
                    self.processor.feed(data)
                    self.renderer.render()
                yield from input_hook()

        loop = asyncio.get_event_loop()
        with focusing_buffer(self.buffer), self.stream.raw_mode():
            loop.run_until_complete(run_async())
