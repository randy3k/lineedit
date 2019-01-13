def get_command(name):
    if name in globals():
        return globals()[name]
    elif name.replace('-', '_') in globals():
        return globals()[name.replace('-', '_')]

    raise KeyError('readline command not found: {}'.format(name))


# Commands For Moving


def beginning_of_line(event):
    event.buffer.document.move_cursor_to_bol()


def end_of_line(event):
    event.buffer.document.move_cursor_to_eol()
