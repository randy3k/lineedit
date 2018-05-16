from __future__ import unicode_literals
import os
import sys
import pexpect
import pyte
import ptyprocess
import threading
import time

examples = os.path.join(os.path.dirname(__file__), "..", "examples")


def test_simple():
    p = pexpect.spawnu(sys.executable, [os.path.join(examples, "simple.py")])
    assert p.readline().startswith("Enter [p/q] to change mode:")
    assert p.expect("p> ", timeout=5) == 0
    p.sendline("q")
    assert p.expect("q> ", timeout=5) == 0
    p.sendline("p")
    assert p.expect("p> ", timeout=5) == 0


def test_history():
    p = ptyprocess.PtyProcess.spawn([sys.executable, os.path.join(examples, "simple.py")])
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

        time.sleep(1)
        assert screen.display[0].startswith("Enter [p/q] to change mode:")
        assert (screen.cursor.x, screen.cursor.y) == (3, 1)
        p.write(b"apple\n")
        time.sleep(0.2)
        assert screen.display[1].startswith("p> apple")
        assert screen.display[2].startswith("p>")
        p.write(b"q\n")
        time.sleep(0.2)
        assert screen.display[3].startswith("q>")
        p.write(b"\x1bOA")  # up
        time.sleep(0.2)
        assert screen.display[3].startswith("q>")
        p.write(b"\x1bOB")  # down
        time.sleep(0.2)
        p.write(b"p\n")
        time.sleep(0.2)
        assert screen.display[4].startswith("p>")
        p.write(b"\x1bOA")  # up
        p.write(b"\x1bOA")  # up
        time.sleep(0.2)
        assert screen.display[4].startswith("p> apple")

    finally:
        p.terminate(force=True)
