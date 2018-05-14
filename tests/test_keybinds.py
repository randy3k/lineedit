from __future__ import unicode_literals
import os
import sys
import pexpect


examples = os.path.join(os.path.dirname(__file__), "..", "examples")


def test_simple():
    p = pexpect.spawnu(sys.executable, [os.path.join(examples, "keybinds.py")])
    assert p.readline().startswith("Enter [p/q/r] to change mode:")
    assert p.expect("p> ", timeout=5) == 0
    p.send("q\n")
    assert p.expect("q> ", timeout=5) == 0
    p.send("r\n")
    assert p.expect("r> ", timeout=5) == 0
    p.send("p\n")
    assert p.expect("p> ", timeout=5) == 0
