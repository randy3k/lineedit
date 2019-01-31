class Layout:

    def __init__(self, message, buf):
        self.message = message
        self.buffer = buf

    def write_to_screen(self, screen):
        indent = " " * len(self.message)
        screen.feed(self.message)
        for i, line in enumerate(self.buffer.text.split('\n')):
            if i > 0:
                screen.feed('\n')
                screen.feed(indent)
            screen.feed(line)

    @property
    def cursor(self):
        """
        This is the cursor position before wrapping
        """
        r, c = self.buffer.document.rowcol
        return (r, c + len(self.message))
