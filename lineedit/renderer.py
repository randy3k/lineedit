class Renderer:
    def __init__(self, layout, console):
        self.layout = layout
        self.console = console
        self._cursor = (0, 0)

    def render(self):
        self.console.hide_cursor()
        # we don't apply erase_down directly to avoid screen being pushed to history
        # in some terminals
        self.console.cursor_up(self._cursor[0])
        self.console.cursor_horizontal_absolute(2)
        self.console.erase_down()
        self.console.cursor_horizontal_absolute(1)
        self.console.erase_end_of_line()

        data = self.layout.serialize(width=self.console.get_size()[1])
        self.console.write_raw(data)

        cursor, (diff_y, diff_x) = self.layout.cursor_offset()
        if diff_y > 0:
            self.console.cursor_up(diff_y)
        else:
            self.console.cursor_down(-diff_y)

        if diff_x > 0:
            self.console.cursor_backward(diff_x)
        else:
            self.console.cursor_forward(-diff_x)

        self._cursor = cursor

        self.console.show_cursor()
        self.console.flush()
