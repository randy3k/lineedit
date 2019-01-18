from .utils import find_nth


class Document:
    _text = None
    _cursor = 0
    _row = 0
    _col = 0

    def __init__(self, initial_text=""):
        self._text = initial_text

    def insert_text(self, text):
        cursor = self.cursor
        self._text = self._text[0:cursor] + text + self._text[cursor:]
        self.cursor = cursor + len(text)

    @property
    def text(self):
        return self._text

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, value):
        self._cursor = value
        text_before_cursor = self._text[0:value]
        self._row = text_before_cursor.count('\n')
        if self._row == 0:
            self._col = len(text_before_cursor)
        else:
            nthlinefeed = find_nth(text_before_cursor, '\n', self._row)
            self._col = len(text_before_cursor) - nthlinefeed - 1

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

    def move_cursor_to_bol(self):
        pass

    def move_cursor_to_eol(self):
        pass


class Buffer:
    def __init__(self):
        self.document = Document()

    def insert_text(self, text):
        self.document.insert_text(text)

    @property
    def text(self):
        return self.document.text
