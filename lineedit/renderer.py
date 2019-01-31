from .screen import Screen


class Renderer:
    def __init__(self, layout, console):
        self.layout = layout
        self.console = console
        self._cursor = (0, 0)

    def render(self):
        screen = Screen(width=self.console.get_size()[1])
        self.layout.write_to_screen(screen)

        self.console.hide_cursor()
        self.console.cursor_up(self._cursor[0])
        self.console.cursor_horizontal_absolute(0)
        self.console.erase_down()
        data = screen.cast()
        self.console.write_raw(data)

        screen_cursor = screen.cursor
        current_cursor = screen.get_wrapped_coordinates(self.layout.cursor)
        diff_y = screen_cursor[0] - current_cursor[0]
        if diff_y > 0:
            self.console.cursor_up(diff_y)
        else:
            self.console.cursor_down(diff_y)
        diff_x = screen_cursor[1] - current_cursor[1]
        if diff_x > 0:
            self.console.cursor_backward(diff_x)
        else:
            self.console.cursor_forward(diff_x)

        self._cursor = current_cursor

        self.console.show_cursor()
        self.console.flush()
