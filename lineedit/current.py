from contextlib import contextmanager


buffer_stack = []


def focus_buffer(buf):
    buffer_stack.append(buf)


def unfocus_buffer(buf):
    buffer_stack.pop()


def current_buffer():
    return buffer_stack[-1]


@contextmanager
def focusing_buffer(buf):
    focus_buffer(buf)
    try:
        yield
    finally:
        unfocus_buffer(buf)
