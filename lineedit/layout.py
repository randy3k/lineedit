from .char import text_to_chars


class Layout:

    def __init__(self, message, buf):
        self.message = message
        self.buffer = buf

    def write_to_screen(self, screen):
        screen.feed(text_to_chars(self.message))
        screen.feed(text_to_chars(self.buffer.text))
