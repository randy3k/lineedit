from .utils import find_nth


class Document:
    _text = None
    _cursor = 0

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
    def text_before_cursor(self):
        return self._text[0:self.cursor]

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, value):
        if value > len(self.text) or value == -1:
            value = len(self.text)
        self._cursor = value

    @property
    def rowcol(self):
        value = self.cursor
        text_before_cursor = self._text[0:value]
        row = self.text_before_cursor.count('\n')
        if row == 0:
            col = len(text_before_cursor)
        else:
            nthlinefeed = find_nth(text_before_cursor, '\n', row)
            col = len(text_before_cursor) - nthlinefeed - 1

        return row, col

    @rowcol.setter
    def rowcol(self, rc):
        r, c = rc
        row = self.text.count('\n')
        if r > row:
            r, c = self.rowcol
        elif r < 0:
            r = 0

        if row == 0:
            self.cursor = c
            return

        linefeed = find_nth(self.text, '\n', r)
        next_linefeed = find_nth(self.text, '\n', r + 1)
        if next_linefeed == -1:
            next_linefeed = len(self.text)

        if c == -1:
            self.cursor = next_linefeed
        else:
            self.cursor = min(linefeed + c + 1, next_linefeed)

    def move_cursor_to_bol(self):
        r, c = self.rowcol
        self.rowcol = (r, 0)

    def move_cursor_to_eol(self):
        r, c = self.rowcol
        self.rowcol = (r, -1)

    def move_cursor_to_left(self, amount=1):
        if self.cursor - amount < 0:
            self.cursor = 0
        else:
            self.cursor = self.cursor - amount

    def move_cursor_to_right(self, amount=1):
        self.cursor = self.cursor + amount

    def move_cursor_up(self, amount=1):
        # TODO: remember column position for consecutive up
        r, c = self.rowcol
        self.rowcol = (r - amount, c)

    def move_cursor_down(self, amount=1):
        r, c = self.rowcol
        self.rowcol = (r + amount, c)


class Buffer:
    def __init__(self):
        self.document = Document()

    def insert_text(self, text):
        self.document.insert_text(text)

    @property
    def text(self):
        return self.document.text

    def auto_up(self):
        self.document.move_cursor_up()

    def auto_down(self):
        self.document.move_cursor_down()
