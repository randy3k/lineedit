from .utils import is_windows
if is_windows():
    from .screen import Win32Screen as Screen
else:
    from .screen import PosixScreen as Screen


class Renderer:
    def __init__(self, layout, console):
        self.layout = layout
        self.console = console
        self.screen_cursor = (0, 0)  # relative to the first line of prompt
        self.console_cursor = None   # relative to the first line of terminal
        self.previous_cast = None
        self.waiting_cpr_response = False

    def render(self):
        screen = Screen(width=self.console.get_size()[1])
        self.layout.write_to_screen(screen)
        data = screen.cast()

        if data == self.previous_cast:
            # TODO: diff screen to write
            # it would happen if we have received data which doens't change the UI, e.g. CPR
            self.console.hide_cursor()
            self.console.cursor_up(self.screen_cursor[0])
            self.console.cursor_horizontal_absolute(0)
            self.console.cursor_down(screen.marked_cursor[0])
            self.console.cursor_forward(screen.marked_cursor[1])
            self.console.show_cursor()
            self.console.flush()
            return

        self.previous_cast = data

        self.console.hide_cursor()
        # we don't apply erase_down directly to avoid screen being pushed to history
        # in some terminals
        self.console.cursor_up(self.screen_cursor[0])
        self.console.cursor_horizontal_absolute(2)
        self.console.erase_down()
        self.console.cursor_horizontal_absolute(1)
        self.console.erase_end_of_line()

        self.console.write_raw(data)
        self.console.cursor_up(len(screen.lines) - 1)
        self.console.cursor_horizontal_absolute(0)
        self.console.cursor_down(screen.marked_cursor[0])
        self.console.cursor_forward(screen.marked_cursor[1])
        self.screen_cursor = screen.marked_cursor
        self.console.show_cursor()
        self.request_console_cursor_position()
        self.console.flush()

    def request_console_cursor_position(self):
        # it should only be called after rendering
        if self.waiting_cpr_response:
            return

        if is_windows():
            r, c = self.console.get_cursor_position()
            self.report_console_cursor_position(r, c)
        else:
            # the key processor will call `report_console_cursor_position`
            self.console.ask_for_cpr()
            self.waiting_cpr_response = True

    def report_console_cursor_position(self, r, c):
        self.waiting_cpr_response = False
        self.console_cursor = (r, c)
