from __future__ import unicode_literals
import os
import sys
from helpers import assert_equal, assert_startswith, PtyProcess, Screen, ByteStream

examples = os.path.join(os.path.dirname(__file__), "..", "examples")


def test_keybinds():
    p = PtyProcess.spawn([sys.executable, os.path.join(examples, "keybinds.py")])
    screen = Screen(p, 80, 24)
    stream = ByteStream(screen)
    stream.start_feeding()

    try:
        assert_startswith(lambda: screen.display[0], "Enter [p/q/r] to change mode:")
        assert_equal(lambda: (screen.cursor.x, screen.cursor.y), (3, 1))
        p.write(b"q")
        assert_startswith(lambda: screen.display[1], "q>")
        p.write(b"r")
        assert_startswith(lambda: screen.display[1], "r>")
        p.write(b"p")
        assert_startswith(lambda: screen.display[1], "p>")
    finally:
        p.terminate(force=True)
