from .char import chars_to_text


class Screen:
    def __init__(self, width):
        self.screen_width = width
        self.cursor = (0, 0)
        self.lines = []
        self.wrapped = []

    def feed(self, chars):
        for c in chars:
            if c.data == "\n":
                self.cursor = (self.cursor[0] + 1, 0)
            elif self.cursor[1] == self.screen_width:
                self.wrapped.append(self.cursor[0])
                self.cursor = (self.cursor[0] + 1, 0)
            if self.cursor[0] >= len(self.lines):
                self.lines = self.lines + [[]] * (self.cursor[0] - len(self.lines) + 1)

            if c.data != "\n":
                self.lines[self.cursor[0]].insert(self.cursor[1], c)
                self.cursor = (self.cursor[0], self.cursor[1] + 1)

    def cast(self):
        for i in reversed(self.wrapped):
            self.lines = self.lines[:i] + [self.lines[i] + self.lines[i + 1]]

        return "\n".join(map(chars_to_text, self.lines))
