import sys
from lineedit import Mode, ModalPromptSession

session = ModalPromptSession()
session.register_mode(Mode("p", message=lambda: "p> "))
session.register_mode(Mode("q", message=lambda: "q> "))
session.register_mode(Mode("r", message=lambda: "r> "))
session.register_mode(Mode("s", message=lambda: "s> "))
session.register_mode(Mode("?", message=lambda: "?> ", is_sticky=False))


print("Enter [p/q/r/s/?] to change mode:")
while True:
    try:
        text = session.prompt()
        if len(text) == 1:
            session.activate_mode(text)
    except EOFError:
        sys.exit(0)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        pass
