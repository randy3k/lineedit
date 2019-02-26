import asyncio
import signal
import sys

from .buffer import Buffer
from .completions import CompletionsMenu
from .current import prompt_change
from .layout import Layout
from .key_bindings import default_bindings
from .key_processor import KeyProcessor
from .utils import is_windows

from .renderer import Renderer
if is_windows():
    from .win32_stream import Win32Stream as Stream
    from .win32_console import Win32Console as Console
else:
    from .posix_stream import PosixStream as Stream
    from .posix_console import PosixConsole as Console


class Prompt:
    def __init__(self, message='', completer=None):
        self._value = None
        self.buffer = Buffer()
        self.search_buffer = Buffer()
        self.completions_menu = CompletionsMenu(self.buffer, completer)

        self.bindings = default_bindings()
        self.processor = KeyProcessor(self.bindings)

        self.stream = Stream(sys.stdin)
        self.console = Console(sys.stdout)

        self.layout = Layout(message, self.buffer, self.search_buffer, self.completions_menu)
        self.renderer = Renderer(self.layout, self.console)

    def run(self):
        self.console.enable_bracketed_paste()
        self.console.enable_autowrap()
        self.console.flush()

        loop = asyncio.get_event_loop()

        def on_resize():
            self.renderer.render()

        async def input_hook():
            while True:
                if self.stream.wait_until_ready(timeout=0):
                    return
                await asyncio.sleep(0.03)

        async def run_async():
            self.renderer.render()

            while True:
                if self.stream.wait_until_ready(timeout=0):
                    data = self.stream.read()
                    self.processor.feed(data)
                    self.renderer.render()

                if self.value is not None:
                    self.console.write("\n")
                    self.console.erase_down()
                    self.console.flush()
                    break

                await input_hook()

        try:
            with prompt_change(self), self.stream.raw_mode():
                if not is_windows():
                    loop.add_signal_handler(signal.SIGWINCH, on_resize)
                loop.run_until_complete(run_async())
        finally:
            loop.close()

    def auto_complete(self):
        self.completions_menu.show()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v
