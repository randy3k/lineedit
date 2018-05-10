# lineedit: A readline library based on prompt_toolkit which supports multiple modes

It provides some subclasses inherited from [prompt_toolkit](https://github.com/jonathanslenders/python-prompt-toolkit) to mimic Julia [LineEdit.jl](https://github.com/JuliaLang/julia/blob/master/stdlib/REPL/src/LineEdit.jl) with multiple modal support.

As prompt_toolkit v2.0 is not out yet, we also ship a copy of it for now.


```py
from lineedit import ModalPromptSession, ModalInMemoryHistory

session = ModalPromptSession(
    history = ModalInMemoryHistory()
)

while True:
    text = session.prompt("> ")
    print(len(text))

```