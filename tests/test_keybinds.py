from __future__ import unicode_literals
import os
import sys
import pyte
import ptyprocess
import threading
import time

examples = os.path.join(os.path.dirname(__file__), "..", "examples")


def test_keybinds():
    p = ptyprocess.PtyProcess.spawn([sys.executable, os.path.join(examples, "keybinds.py")])
    screen = pyte.Screen(80, 24)
    screen.write_process_input = lambda s: p.write(s.encode())
    stream = pyte.ByteStream(screen)

    def reader():
        while True:
            try:
                data = p.read(1024)
            except EOFError:
                break
            if data:
                stream.feed(data)

    try:
        t = threading.Thread(target=reader)
        t.start()

        time.sleep(0.5)
        assert screen.display[0].startswith("Enter [p/q/r] to change mode:")
        assert (screen.cursor.x, screen.cursor.y) == (3, 1)
        p.write(b"q")
        time.sleep(0.1)
        assert screen.display[1].startswith("q>")
        p.write(b"r")
        time.sleep(0.1)
        assert screen.display[1].startswith("r>")
        p.write(b"p")
        time.sleep(0.1)
        assert screen.display[1].startswith("p>")
    finally:
        p.terminate(force=True)
