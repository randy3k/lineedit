from __future__ import unicode_literals
import sys
from lineedit import Mode, ModalPromptSession
from prompt_toolkit.key_binding.key_bindings import KeyBindings
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.filters import has_focus


session = ModalPromptSession()

default_focused = has_focus(DEFAULT_BUFFER)

pkb = KeyBindings()
@pkb.add('q', filter = default_focused)
def _(event):
    session.change_mode("q")


qkb = KeyBindings()
@qkb.add('p', filter = default_focused)
def _(event):
    session.change_mode("p")


rkb = KeyBindings()
@rkb.add('p', filter = default_focused)
def _(event):
    session.change_mode("p")
@rkb.add('q', filter = default_focused)
def _(event):
    session.change_mode("q")


kb = KeyBindings()
@kb.add('r', filter = default_focused)
def _(event):
    session.change_mode("r")


session.register_mode(Mode("p", message=lambda: "p> ", prompt_key_bindings=pkb))
session.register_mode(Mode("q", message=lambda: "q> ", prompt_key_bindings=qkb))
session.register_mode(Mode("r", message=lambda: "r> ", key_bindings=kb, prompt_key_bindings=rkb))


print("Enter [p/q/r] to change mode:")
while True:
    try:
        text = session.prompt()
    except EOFError:
        sys.exit(0)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        pass
