import re

from .utils import find_nth


PREVIOUS_WORD_BOUNDARY = re.compile(r"\b(?=\w)")
NEXT_WORD_BOUNDARY = re.compile(r"(?<=\w)\b")


class Document:
    _text = None
    _cursor = 0

    def __init__(self, initial_text=""):
        self._text = initial_text

    def insert_text(self, text):
        cursor = self.cursor
        self._text = self._text[0:cursor] + text + self._text[cursor:]
        self.cursor = cursor + len(text)

    def delete_char(self, forward=False):
        # TODO: support kill ring
        cursor = self.cursor
        if forward:
            self._text = self._text[0:cursor] + self._text[cursor + 1:]
            self.cursor = cursor
        else:
            self._text = self._text[0:cursor - 1] + self._text[cursor:]
            self.cursor = cursor - 1

    @property
    def text(self):
        return self._text

    @property
    def text_before_cursor(self):
        return self._text[0:self.cursor]

    @property
    def text_after_cursor(self):
        return self._text[self.cursor:]

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, value):
        if value > len(self.text):
            value = len(self.text)
        elif value < 0:
            value = 0
        self._cursor = value

    def rowcol(self, cursor=None):
        if cursor is None:
            cursor = self.cursor
        text_before_cursor = self._text[0:cursor]
        row = self.text_before_cursor.count('\n')
        if row == 0:
            col = len(text_before_cursor)
        else:
            nthlinefeed = find_nth(text_before_cursor, '\n', row)
            col = len(text_before_cursor) - nthlinefeed - 1

        return row, col

    def text_point(self, r, c):
        row = self.text.count('\n')
        if r > row:
            r, c = self.rowcol
        elif r < 0:
            r = 0

        if row == 0:
            if c == -1:
                c = len(self.text) - 1
            return (0, c)

        linefeed = find_nth(self.text, '\n', r)
        next_linefeed = find_nth(self.text, '\n', r + 1)
        if next_linefeed == -1:
            next_linefeed = len(self.text)

        if c == -1:
            return next_linefeed
        else:
            return min(linefeed + c + 1, next_linefeed)

    def move_cursor_to_bol(self):
        r, c = self.rowcol()
        self.cursor = self.text_point(r, 0)

    def move_cursor_to_eol(self):
        r, c = self.rowcol()
        self.cursor = self.text_point(r, -1)

    def move_cursor_to_left(self, amount=1):
        if self.cursor - amount < 0:
            self.cursor = 0
        else:
            self.cursor = self.cursor - amount

    def move_cursor_to_right(self, amount=1):
        self.cursor = self.cursor + amount

    def move_cursor_up(self, amount=1):
        # TODO: remember column position for consecutive up
        r, c = self.rowcol()
        self.cursor = self.text_point(r - amount, c)

    def move_cursor_down(self, amount=1):
        r, c = self.rowcol()
        self.cursor = self.text_point(r + amount, c)

    def _previous_word_position(self):
        text_before_cursor = self.text_before_cursor
        pos = [it.start() for it in PREVIOUS_WORD_BOUNDARY.finditer(text_before_cursor)]
        if pos:
            return pos[-1]
        else:
            return -1

    def move_cursor_to_previous_word(self):
        pos = self._previous_word_position()
        if pos >= 0:
            self.cursor = pos

    def delete_previous_word(self):
        pos = self._previous_word_position()
        if pos >= 0:
            self._text = self._text[:pos] + self.text_after_cursor
            self.cursor = pos

    def _next_word_position(self):
        text_after_cursor = self.text_after_cursor
        m = NEXT_WORD_BOUNDARY.search(text_after_cursor)
        if m:
            return self.cursor + m.start()
        else:
            return -1

    def move_cursor_to_next_word(self):
        pos = self._next_word_position()
        if pos >= 0:
            self.cursor = pos


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
