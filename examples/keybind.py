import sys
from lineedit import Mode, ModalPromptSession
from prompt_toolkit.key_binding.key_bindings import KeyBindings
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.filters import has_focus


session = ModalPromptSession()

default_focused = has_focus(DEFAULT_BUFFER)

pkb = KeyBindings()
@pkb.add('c-f', filter = default_focused)
def _(event):
    session.change_mode("q")


qkb = KeyBindings()
@qkb.add('c-g', filter = default_focused)
def _(event):
    session.change_mode("p")


session.register_mode(Mode("p", message=lambda: "p> ", key_bindings=pkb))
session.register_mode(Mode("q", message=lambda: "q> ", key_bindings=qkb))


print("Enter [ctrl-f/g] to change mode:")
while True:
    try:
        text = session.prompt()
    except EOFError:
        sys.exit(0)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        pass
