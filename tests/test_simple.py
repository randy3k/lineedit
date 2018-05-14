from __future__ import unicode_literals
import os
import sys
import pexpect

examples = os.path.join(os.path.dirname(__file__), "..", "examples")


def test_simple():
    p = pexpect.spawnu(sys.executable, [os.path.join(examples, "simple.py")])
    assert p.readline().startswith("Enter [p/q] to change mode:")
    assert p.expect("p> ", timeout=5) == 0
    p.sendline("q")
    assert p.expect("q> ", timeout=5) == 0
    p.sendline("p")
    assert p.expect("p> ", timeout=5) == 0
