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
    # enable bracketed paste mode
    sys.stdout.write('\x1b[?2004h')
    sys.stdout.flush()


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
            if data and data[0].key == Key.ControlD:
                return
            if data:
                print(data)
                continue
        yield from input_hook()


loop = asyncio.get_event_loop()
with stream.raw_mode():
    loop.run_until_complete(run_async())
