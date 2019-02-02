from .screen import Screen


class Layout:

    def __init__(self, message, buf):
        self.message = message
        self.buffer = buf
        self.screen = None

    def serialize(self, width):
        screen = Screen(width)
        self.screen = screen
        indent = " " * len(self.message)
        screen.feed(self.message)
        for i, line in enumerate(self.buffer.text.split('\n')):
            if i > 0:
                screen.feed('\n')
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
        return self.wrapped_coordinates(unwrapped)

    def wrapped_coordinates(self, unwrapped):
        """
        Get the wrapped coordinates on screen from unwrapped coordinates
        """
        # TODO: support wide chars

        if not self.screen:
            return unwrapped

        width = self.screen.width
        lines = self.screen.lines
        wrapped = self.screen.wrapped

        r, c = unwrapped
        row = 0
        for i in range(len(lines)):
            if row == r:
                if c < width:
                    return i, c
                elif i in wrapped:
                    c -= width
                else:
                    return i, width
            if i not in wrapped:
                row += 1

    def cursor_offset(self):
        screen_cursor = self.screen.cursor
        current_cursor = self.cursor

        diff_y = screen_cursor[0] - current_cursor[0]
        diff_x = screen_cursor[1] - current_cursor[1]

        return current_cursor, (diff_y, diff_x)
