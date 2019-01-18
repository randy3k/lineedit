from .screen import Screen


class Renderer:
    def __init__(self, layout, console):
        self.layout = layout
        self.console = console
        self._cursor = (0, 0)

    def render(self):
        screen = Screen(width=self.console.get_size()[0])
        self.layout.write_to_screen(screen)

        self.console.cursor_up(self._cursor[1])
        self.console.cursor_horizontal_absolute(0)
        self.console.erase_down()
        data = screen.display()
        self.console.write_raw(data)
        data_len = len(data)
        row, col = self.console.get_size()
        if data_len > 0:
            self._cursor = (data_len - 1) % col + 1, (data_len - 1) // col
        else:
            self._cursor = 0, 0

        with open("/tmp/lineedit", "a") as f:
            f.write(str(self._cursor))
            f.write("\n")
        self.console.flush()
