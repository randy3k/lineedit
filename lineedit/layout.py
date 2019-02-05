from .screen import Win32Screen, PosixScreen
from .utils import is_windows


class Layout:

    def __init__(self, message, buf):
        self.message = message
        self.buffer = buf
        self.screen = None

    def serialize(self, width):
        if is_windows():
            self.screen = Win32Screen(width)
        else:
            self.screen = PosixScreen(width)

        screen = self.screen
        indent = " " * len(self.message)
        screen.feed(self.message)
        for i, line in enumerate(self.buffer.text.split('\n')):
            if i > 0:
                screen.feed('\n')
                if len(line) > 0:
                    screen.feed(indent)
            screen.feed(line)
        return screen.cast()

    @property
    def cursor(self):
        """
        This is the cursor position after wrapping
        """
        r, c = self.buffer.document.rowcol
        unwrapped = (r, c + len(self.message))

        if self.screen:
            return self.screen.wrapped_coordinates(unwrapped)
        else:
            return unwrapped

    def cursor_offset(self):
        screen_cursor = self.screen.cursor
        current_cursor = self.cursor

        diff_y = screen_cursor[0] - current_cursor[0]
        diff_x = screen_cursor[1] - current_cursor[1]

        return current_cursor, (diff_y, diff_x)
