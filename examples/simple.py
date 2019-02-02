from lineedit.prompt import Prompt


p = Prompt("> ")
p.run()
print("we get " + p.value)
