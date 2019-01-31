class Layout:

    def __init__(self, message, buf):
        self.message = message
        self.buffer = buf

    def write_to_screen(self, screen):
        screen.feed(self.message)
        screen.feed(self.buffer.text)

    @property
    def cursor(self):
        self.buffer.document.cursor
