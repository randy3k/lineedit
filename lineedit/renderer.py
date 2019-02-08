from .screen import Win32Screen, PosixScreen
from .utils import is_windows


class Renderer:
    def __init__(self, layout, console):
        self.layout = layout
        self.console = console
        self._cursor = (0, 0)

    def render(self):
        if is_windows():
            screen = Win32Screen(width=self.console.get_size()[1])
        else:
            screen = PosixScreen(width=self.console.get_size()[1])

        self.console.hide_cursor()
        # we don't apply erase_down directly to avoid screen being pushed to history
        # in some terminals
        self.console.cursor_up(self._cursor[0])
        self.console.cursor_horizontal_absolute(2)
        self.console.erase_down()
        self.console.cursor_horizontal_absolute(1)
        self.console.erase_end_of_line()

        self.layout.write_to_screen(screen)

        data = screen.cast()
        self.console.write_raw(data)

        diff_y = screen.cursor[0] - screen.marked_cursor[0]
        if diff_y > 0:
            self.console.cursor_up(diff_y)
        else:
            self.console.cursor_down(-diff_y)

        diff_x = screen.cursor[1] - screen.marked_cursor[1]
        if diff_x > 0:
            self.console.cursor_backward(diff_x)
        else:
            self.console.cursor_forward(-diff_x)

        self._cursor = screen.marked_cursor

        self.console.show_cursor()
        self.console.flush()
