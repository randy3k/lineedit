from __future__ import unicode_literals
import os
import sys
from helpers import assert_equal, assert_startswith, PtyProcess, Screen, ByteStream

examples = os.path.join(os.path.dirname(__file__), "..", "examples")


if not sys.platform.startswith("win"):
    import pexpect

    def test_simple():
        p = pexpect.spawnu(sys.executable, [os.path.join(examples, "simple.py")])
        assert p.readline().startswith("Enter [p/q] to change mode:")
        assert p.expect("p> ", timeout=5) == 0
        p.sendline("q")
        assert p.expect("q> ", timeout=5) == 0
        p.sendline("p")
        assert p.expect("p> ", timeout=5) == 0


def test_history():
    p = PtyProcess.spawn([sys.executable, os.path.join(examples, "simple.py")])
    screen = Screen(p, 80, 24)
    stream = ByteStream(screen)
    stream.start_feeding()

    try:
        assert_startswith(lambda: screen.display[0], "Enter [p/q] to change mode:")
        assert_equal(lambda: (screen.cursor.x, screen.cursor.y), (3, 1))
        p.write(b"apple\n")
        assert_startswith(lambda: screen.display[1], "p> apple")
        assert_startswith(lambda: screen.display[2], "p>")
        p.write(b"q\n")
        assert_startswith(lambda: screen.display[3], "q>")
        p.write(b"\x1bOA")  # up
        assert_startswith(lambda: screen.display[3], "q>")
        p.write(b"\x1bOB")  # down
        p.write(b"p\n")
        assert_startswith(lambda: screen.display[4], "p>")
        p.write(b"\x1bOA")  # up
        p.write(b"\x1bOA")  # up
        assert_startswith(lambda: screen.display[4], "p> apple")
    finally:
        p.terminate(force=True)
