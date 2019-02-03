from .char import text_to_chars, chars_to_text, Char
from .utils import is_windows


class PosixScreen:
    def __init__(self, width):
        self.width = width
        self.cursor = (0, 0)
        self.lines = []
        self.wrapped = []

    def feed(self, chars):
        for c in text_to_chars(chars):
            if c.data == "\n":
                self.cursor = (self.cursor[0] + 1, 0)
            elif self.cursor[1] == self.width:
                self.wrapped.append(self.cursor[0])
                self.cursor = (self.cursor[0] + 1, 0)

            if self.cursor[0] >= len(self.lines):
                self.lines = self.lines + [[]] * (self.cursor[0] - len(self.lines) + 1)

            if c.data != "\n":
                self.lines[self.cursor[0]].insert(self.cursor[1], c)
                self.cursor = (self.cursor[0], self.cursor[1] + 1)

    def cast(self):
        lines = self.lines[:]
        for i in reversed(self.wrapped):
            lines = lines[:i] + [lines[i] + lines[i + 1]] + lines[i + 2:]

        return "\n".join(map(chars_to_text, lines))


class Win32Screen:
    def __init__(self, width):
        self.width = width
        self.cursor = (0, 0)
        self.lines = []
        self.wrapped = []

    def feed(self, chars):
        for c in text_to_chars(chars):
            if self.cursor[1] == self.width:
                self.cursor = (self.cursor[0] + 1, 0)
            if c.data == "\n":
                self.cursor = (self.cursor[0] + 1, 0)
            elif self.cursor[1] == self.width - 1:
                self.wrapped.append(self.cursor[0])

            if self.cursor[0] >= len(self.lines):
                self.lines = self.lines + [[]] * (self.cursor[0] - len(self.lines) + 1)
            elif self.cursor[0] in self.wrapped and self.cursor[0] + 1 >= len(self.lines):
                self.lines = self.lines + [[]] * (self.cursor[0] - len(self.lines) + 2)

            if c.data != "\n":
                self.lines[self.cursor[0]].insert(self.cursor[1], c)
                self.cursor = (self.cursor[0], self.cursor[1] + 1)

    def cast(self):
        lines = self.lines[:]
        for i in reversed(self.wrapped):
            lines = lines[:i] + [lines[i] + lines[i + 1]] + lines[i + 2:]

        for l, line in enumerate(lines):
            if line and len(line) % self.width == 0:
                c = line[-1]
                new_line = Char('\n', c.fg, c.bg, c.bold, c.underline, c.blink, c.reverse)
                lines[l] += [new_line]

        return "\n".join(map(chars_to_text, lines))


if is_windows():
    Screen = Win32Screen
else:
    Screen = PosixScreen
