from .screen import Screen


class Renderer:
    def __init__(self, layout, console):
        self.layout = layout
        self.console = console
        self._cursor = (0, 0)

    def render(self):
        screen = Screen(width=self.console.get_size()[1])
        self.layout.write_to_screen(screen)

        self.console.cursor_up(self._cursor[0])
        self.console.cursor_horizontal_absolute(0)
        self.console.erase_down()
        data = screen.cast()
        self.console.write_raw(data)
        self._cursor = screen.cursor

        self.console.flush()
