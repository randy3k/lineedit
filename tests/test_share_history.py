from __future__ import unicode_literals
import os
import sys
from helpers import assert_equal, assert_startswith, PtyProcess, Screen, ByteStream

examples = os.path.join(os.path.dirname(__file__), "..", "examples")


def test_history():
    p = PtyProcess.spawn([sys.executable, os.path.join(examples, "share_history.py")])
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
        assert_startswith(lambda: screen.display[3], "p> q")
        p.write(b"\x1bOB")  # down
        assert_startswith(lambda: screen.display[3], "q>")
        p.write(b"\x1bOA")  # up
        p.write(b"\x1bOA")  # up
        assert_startswith(lambda: screen.display[3], "p> apple")
        p.sendintr()
        assert_startswith(lambda: screen.display[4], "q>")
    finally:
        p.terminate(force=True)
