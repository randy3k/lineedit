from .char import text_to_chars, chars_to_text, dup_char


class Screen:
    def __init__(self, width):
        self.width = width
        self.cursor = (0, 0)
        self.lines = []
        self.wrapped = []

    def wrapped_coordinates(self, unwrapped):
        """
        Get the wrapped coordinates on screen from unwrapped coordinates
        """
        # TODO: support wide chars

        width = self.width
        wrapped = self.wrapped

        r, c = unwrapped
        row = 0
        for i in range(len(self.lines)):
            if row == r:
                if c < width:
                    return i, c
                elif i in wrapped:
                    c -= width
                else:
                    return i, width
            if i not in wrapped:
                row += 1


class PosixScreen(Screen):
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


class Win32Screen(Screen):
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
                lines[l] += [dup_char(line[-1], "\n")]

        return "\n".join(map(chars_to_text, lines))
