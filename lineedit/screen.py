from .char import text_to_chars, chars_to_text


class Screen:
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

    def get_wrapped_coordinates(self, unwrapped):
        """
        Get the coordinate on screen from unwrapped row, col pair
        """
        # TODO: support wide chars
        r, c = unwrapped
        row = 0
        for i in range(len(self.lines)):
            if row == r:
                if c < self.width:
                    return i, c
                elif i in self.wrapped:
                    c -= self.width
                else:
                    return i, self.width
            if i not in self.wrapped:
                row += 1
