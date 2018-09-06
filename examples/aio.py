from lineedit.key import Key
import sys
import time
import asyncio

if sys.platform.startswith("win"):
    import lineedit.win32_stream
    stream = lineedit.win32_stream.Win32Stream(sys.stdin)
else:
    import lineedit.posix_stream
    stream = lineedit.posix_stream.PosixStream(sys.stdin)


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
            print(data)
            if data and data[0] == Key.ControlD:
                return
        else:
            yield from input_hook()


loop = asyncio.get_event_loop()
with stream.raw_mode():
    loop.run_until_complete(run_async())
