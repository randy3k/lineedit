from collections import namedtuple


class Char(namedtuple(
        "Char", ["data", "fg", "bg", "bold", "italic", "underline", "blink", "reverse"])):
    __slots__ = ()

    def __new__(
            cls, data, fg='default', bg='default',
            bold=False, italic=False, underline=False, blink=False, reverse=False):
        return super(Char, cls).__new__(
            cls, data, fg, bg, bold, italic, underline, blink, reverse)


class Screen:
    def __init__(self, width):
        self.screen_width = width
        self.lines = []

    def feed(self, data):
        if len(self.lines) == 0:
            self.lines.append('')

        for c in data:
            if c != "\n":
                self.lines[-1] += c
            else:
                self.lines.append('')

    def display(self):
        return "\n".join(self.lines)
