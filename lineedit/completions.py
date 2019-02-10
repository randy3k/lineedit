from .char import Char

class CompletionsMenu:
    def __init__(self, completer=None):
        self.completer = completer

    def set_completions(self, document):
        self._completions = self.completer.get_completions(document)

    def write_to_screen(self, screen):
        xpos = screen.marked_cursor[1]
        ypos = screen.marked_cursor[0] + 1
        width = min(10, screen.width - xpos - 1)
        height = 3
        for i in range(height):
            for j in range(width):
                screen.draw_at(ypos + i, xpos + j, Char("x", reverse=True))
