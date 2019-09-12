from __future__ import unicode_literals
import sys
from lineedit import ModalPromptSession

session = ModalPromptSession()
session.register_mode("p", message=lambda: "p> ")
session.register_mode("q", message=lambda: "q> ")


print("Enter [p/q] to change mode:")
while True:
    try:
        text = session.prompt()
        session.activate_mode(text)
    except EOFError:
        sys.exit(0)
    except KeyboardInterrupt:
        pass
    except Exception:
        pass
