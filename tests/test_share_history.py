from __future__ import unicode_literals
import os
import sys
import pyte
import ptyprocess
import threading
import time

examples = os.path.join(os.path.dirname(__file__), "..", "examples")


def test_keybinds():
    p = ptyprocess.PtyProcess.spawn([sys.executable, os.path.join(examples, "share_history.py")])
    screen = pyte.Screen(80, 24)
    screen.write_process_input = lambda s: p.write(s.encode())
    stream = pyte.ByteStream(screen)
    loop = [True]

    def reader():
        while loop[0]:
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
        assert screen.display[0].startswith("Enter [p/q] to change mode:")
        assert (screen.cursor.x, screen.cursor.y) == (3, 1)
        p.write("apple\n".encode())
        time.sleep(0.1)
        assert screen.display[1].startswith("p> apple")
        assert screen.display[2].startswith("p>")
        p.write("q\n".encode())
        time.sleep(0.1)
        assert screen.display[3].startswith("q>")
        p.write(b"\x1bOA")  # up
        time.sleep(0.1)
        assert screen.display[3].startswith("p> q")
        p.write(b"\x1bOB")  # up
        time.sleep(0.1)
        assert screen.display[3].startswith("q>")
        p.write(b"\x1bOA")  # up
        p.write(b"\x1bOA")  # up
        time.sleep(0.1)
        assert screen.display[3].startswith("p> apple")
        p.sendintr()
        time.sleep(0.1)
        assert screen.display[4].startswith("q>")

    finally:
        p.terminate(force=True)