from .char import Char


class CompletionsMenu:
    def __init__(self, buf, completer=None):
        self.buffer = buf
        self.completer = completer
        self.hidden = True

    def show(self):
        self._completions = list(self.completer.get_completions(self.buffer.document))
        if self._completions:
            self.hidden = False
        else:
            self.hidden = True

    def hide(self):
        self._completions = []
        self.hidden = True

    def write_to_screen(self, screen):
        if self.hidden:
            return

        xpos = screen.marked_cursor[1]
        ypos = screen.marked_cursor[0] + 1

        max_completion_len = max(len(c) for c, _ in self._completions)
        width = min(max_completion_len + 3, screen.width - xpos - 1)
        height = min(len(self._completions), 3)

        for i in range(height):
            item, offset = self._completions[i]
            screen.draw_at(ypos + i, xpos, Char(" ", bg="light_white"))
            for j in range(width):
                screen.draw_at(ypos + i, xpos + j + 1, Char(" ", fg="light_black", bg="light_white"))
            for j in range(len(item)):
                screen.draw_at(ypos + i, xpos + j + 1, Char(item[j], fg="light_black", bg="light_white"))

            screen.draw_at(ypos + i, xpos + width + 1, Char(" ", bg="light_black"))
