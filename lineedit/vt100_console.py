class Vt100Console:

    def __init__(self, stdout, term="linux"):
        self._buffer = []
        self.stdout = stdout
        self.term = term

    def fileno(self):
        return self.stdout.fileno()

    def encoding(self):
        return self.stdout.encoding

    def get_size(self):
        pass

    def write_raw(self, data):
        self._buffer.append(data)

    def write(self, data):
        self._buffer.append(data.replace('\x1b', '?'))

    def set_title(self, title):
        if self.term not in ('linux', 'eterm-color'):
            self.write_raw('\x1b]2;%s\x07'.format(title.replace('\x1b', '').replace('\x07', '')))

    def clear_title(self):
        self.set_title('')

    def erase_screen(self):
        self.write_raw('\x1b[2J')

    def enter_alternate_screen(self):
        self.write_raw('\x1b[?1049h\x1b[H')

    def quit_alternate_screen(self):
        self.write_raw('\x1b[?1049l')

    def erase_end_of_line(self):
        self.write_raw('\x1b[K')

    def erase_down(self):
        self.write_raw('\x1b[J')

    def disable_autowrap(self):
        self.write_raw('\x1b[?7l')

    def enable_autowrap(self):
        self.write_raw('\x1b[?7h')

    def enable_bracketed_paste(self):
        self.write_raw('\x1b[?2004h')

    def disable_bracketed_paste(self):
        self.write_raw('\x1b[?2004l')

    def cursor_goto(self, row=0, column=0):
        self.write_raw('\x1b[%i;%iH' % (row, column))

    def cursor_up(self, amount):
        if amount == 0:
            pass
        elif amount == 1:
            self.write_raw('\x1b[A')
        else:
            self.write_raw('\x1b[%iA' % amount)

    def cursor_down(self, amount):
        if amount == 0:
            pass
        elif amount == 1:
            self.write_raw('\x1b[B')
        else:
            self.write_raw('\x1b[%iB' % amount)

    def cursor_forward(self, amount):
        if amount == 0:
            pass
        elif amount == 1:
            self.write_raw('\x1b[C')
        else:
            self.write_raw('\x1b[%iC' % amount)

    def cursor_backward(self, amount):
        if amount == 0:
            pass
        elif amount == 1:
            self.write_raw('\b')  # '\x1b[D'
        else:
            self.write_raw('\x1b[%iD' % amount)

    def cursor_horizontal_absolute(self, column):
        self.write_raw('\x1b[%iG' % column)

    def hide_cursor(self):
        self.write_raw('\x1b[?25l')

    def show_cursor(self):
        self.write_raw('\x1b[?12l\x1b[?25h')

    def flush(self):
        if not self._buffer:
            return

        data = ''.join(self._buffer).encode(self.stdout.encoding or 'utf-8', 'replace')
        self.stdout.buffer.write(data)
        self.stdout.flush()

        self._buffer = []

    def ask_for_cpr(self):
        self.write_raw('\x1b[6n')
        self.flush()

    def bell(self):
        self.write_raw('\a')
        self.flush()
