from .char import text_to_chars


class Layout:

    def __init__(self, message, buf, search_buffer, completions_menu):
        self.message = message
        self.buffer = buf
        self.search_buffer = search_buffer
        self.completions_menu = completions_menu
        self.screen = None

    def write_to_screen(self, screen):
        indent = " " * len(self.message)
        screen.feed(text_to_chars(self.message))
        screen.mark()
        r, c = self.buffer.document.rowcol()
        for i, line in enumerate(self.buffer.text.split('\n')):
            if i > 0:
                screen.feed(text_to_chars('\n'))
                screen.feed(text_to_chars(indent))

            chars = list(text_to_chars(line))
            if i == r:
                screen.feed(chars[:c])
                screen.mark()
                screen.feed(chars[c:])
            else:
                screen.feed(chars)

        self.completions_menu.write_to_screen(screen)
