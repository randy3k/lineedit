import os
import sys
import pexpect

examples = os.path.join(os.path.dirname(__file__), "..", "examples")


def test_simple():
    p = pexpect.spawn(sys.executable, [os.path.join(examples, "simple.py")])
    assert p.readline().decode().startswith("Enter [p/q] to change mode:")
    assert p.expect("p> ", timeout=5) == 0
    p.sendline("q")
    assert p.expect("q> ", timeout=5) == 0
    p.sendline("p")
    assert p.expect("p> ", timeout=5) == 0
