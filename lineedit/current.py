from contextlib import contextmanager


buffer_stack = []


def register_buffer(buf):
    buffer_stack.append(buf)


def deregister_buffer(buf):
    buffer_stack.pop()


def current_buffer():
    return buffer_stack[-1]


@contextmanager
def changing_buffer(buf):
    register_buffer(buf)
    try:
        yield
    finally:
        deregister_buffer(buf)
