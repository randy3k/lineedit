class Document:
    _text = None
    _cursor = None

    def insert_text(self, text):
        pass

    def move_cursor_to_bol(self):
        pass

    def move_cursor_to_eol(self):
        pass


class Buffer:
    def __init__(self):
        self.document = Document()

    def insert_text(self, text):
        self.document.insert_text(text)
