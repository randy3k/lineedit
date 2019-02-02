import asyncio
import signal
import sys

from .buffer import Buffer
from .current import prompt_change
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
        self._value = None
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

        loop = asyncio.get_event_loop()

        def on_resize():
            self.renderer.render()

        async def input_hook():
            while True:
                if self.stream.wait_until_ready(timeout=0):
                    return
                await asyncio.sleep(0.03)

        async def run_async():
            while True:
                if self.stream.wait_until_ready(timeout=0):
                    data = self.stream.read()
                    self.processor.feed(data)
                    self.renderer.render()
                if self.value is not None:
                    self.console.write("\n")
                    self.console.flush()
                    break
                await input_hook()

        try:
            with prompt_change(self), self.stream.raw_mode():
                loop.add_signal_handler(signal.SIGWINCH, on_resize)
                loop.run_until_complete(run_async())
        finally:
            loop.close()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v
