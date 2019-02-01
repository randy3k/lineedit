from contextlib import contextmanager


prompt_stack = []


def add_prompt(prompt):
    prompt_stack.append(prompt)


def remove_app(prompt):
    prompt_stack.pop()


def current_prompt():
    return prompt_stack[-1]


@contextmanager
def app_change(prompt):
    add_prompt(prompt)
    try:
        yield
    finally:
        remove_app(prompt)
