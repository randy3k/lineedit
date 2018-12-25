import sys
import time
import asyncio

from lineedit.key_bindings import KeyBindings
from lineedit.key_processor import KeyProcessor
from lineedit.readline import get_command


if sys.platform.startswith("win"):
    import lineedit.win32_stream
    stream = lineedit.win32_stream.Win32Stream(sys.stdin)
else:
    import lineedit.posix_stream
    stream = lineedit.posix_stream.PosixStream(sys.stdin)
    # enable bracketed paste mode
    sys.stdout.write('\x1b[?2004h')
    sys.stdout.flush()


bind = KeyBindings()
processor = KeyProcessor(bind)

bind.add('c-a')(get_command('beginning-of-line'))
bind.add('c-e')(get_command('end-of-line'))


@asyncio.coroutine
def input_hook():
    while True:
        if stream.wait_until_ready(timeout=0):
            return
        time.sleep(0.03)


@asyncio.coroutine
def run_async():
    while True:
        if stream.wait_until_ready(timeout=0):
            data = stream.read()
            processor.feed(data)
        yield from input_hook()


loop = asyncio.get_event_loop()
with stream.raw_mode():
    loop.run_until_complete(run_async())
