import errno


def _get_size(fileno):
    # Thanks to fabric (fabfile.org), and
    # http://sqizit.bartletts.id.au/2011/02/14/pseudo-terminals-in-python/
    import fcntl
    import termios

    buf = array.array(b'h' if six.PY2 else u'h', [0, 0, 0, 0])
    fcntl.ioctl(fileno, termios.TIOCGWINSZ, buf)

    return buf[0], buf[1]

class PosixScreen:

    def __init__(self, stdout, term="linux"):
        self._buffer = []
        self.stdout = stdout
        self.term = term

    def fileno(self):
        """
        Return file descriptor.
        """
        return self.stdout.fileno()

    def encoding(self):
        """
        Return encoding used for stdout.
        """
        return self.stdout.encoding

    def get_size(self):
        return _get_size(self.fileno())


    def write_raw(self, data):
        """
        Write raw data to output.
        """
        self._buffer.append(data)

    def write(self, data):
        """
        Write text to output.
        (Removes vt100 escape codes. -- used for safely writing text.)
        """
        self._buffer.append(data.replace('\x1b', '?'))

    def set_title(self, title):
        """
        Set terminal title.
        """
        if self.term not in ('linux', 'eterm-color'):  # Not supported by the Linux console.
            self.write_raw('\x1b]2;%s\x07' % title.replace('\x1b', '').replace('\x07', ''))

    def clear_title(self):
        self.set_title('')

    def erase_screen(self):
        """
        Erases the screen with the background colour and moves the cursor to
        home.
        """
        self.write_raw('\x1b[2J')

    def enter_alternate_screen(self):
        self.write_raw('\x1b[?1049h\x1b[H')

    def quit_alternate_screen(self):
        self.write_raw('\x1b[?1049l')

    def enable_mouse_support(self):
        self.write_raw('\x1b[?1000h')

        # Enable urxvt Mouse mode. (For terminals that understand this.)
        self.write_raw('\x1b[?1015h')

        # Also enable Xterm SGR mouse mode. (For terminals that understand this.)
        self.write_raw('\x1b[?1006h')

        # Note: E.g. lxterminal understands 1000h, but not the urxvt or sgr
        #       extensions.

    def disable_mouse_support(self):
        self.write_raw('\x1b[?1000l')
        self.write_raw('\x1b[?1015l')
        self.write_raw('\x1b[?1006l')

    def erase_end_of_line(self):
        """
        Erases from the current cursor position to the end of the current line.
        """
        self.write_raw('\x1b[K')

    def erase_down(self):
        """
        Erases the screen from the current line down to the bottom of the
        screen.
        """
        self.write_raw('\x1b[J')

    def reset_attributes(self):
        self.write_raw('\x1b[0m')

    def set_attributes(self, attrs, color_depth):
        """
        Create new style and output.

        :param attrs: `Attrs` instance.
        """
        # Get current depth.
        escape_code_cache = self._escape_code_caches[color_depth]

        # Write escape character.
        self.write_raw(escape_code_cache[attrs])

    def disable_autowrap(self):
        self.write_raw('\x1b[?7l')

    def enable_autowrap(self):
        self.write_raw('\x1b[?7h')

    def enable_bracketed_paste(self):
        self.write_raw('\x1b[?2004h')

    def disable_bracketed_paste(self):
        self.write_raw('\x1b[?2004l')

    def cursor_goto(self, row=0, column=0):
        """ Move cursor position. """
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
            # Note: Not the same as '\n', '\n' can cause the window content to
            #       scroll.
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

    def hide_cursor(self):
        self.write_raw('\x1b[?25l')

    def show_cursor(self):
        self.write_raw('\x1b[?12l\x1b[?25h')  # Stop blinking cursor and show.

    def flush(self):
        """
        Write to output stream and flush.
        """
        if not self._buffer:
            return

        data = ''.join(self._buffer)

        try:
            # (We try to encode ourself, because that way we can replace
            # characters that don't exist in the character set, avoiding
            # UnicodeEncodeError crashes. E.g. u'\xb7' does not appear in 'ascii'.)
            # My Arch Linux installation of july 2015 reported 'ANSI_X3.4-1968'
            # for sys.stdout.encoding in xterm.
            if self.write_binary:
                if hasattr(self.stdout, 'buffer'):
                    out = self.stdout.buffer  # Py3.
                else:
                    out = self.stdout
                out.write(data.encode(self.stdout.encoding or 'utf-8', 'replace'))
            else:
                self.stdout.write(data)

            self.stdout.flush()
        except IOError as e:
            if e.args and e.args[0] == errno.EINTR:
                # Interrupted system call. Can happen in case of a window
                # resize signal. (Just ignore. The resize handler will render
                # again anyway.)
                pass
            elif e.args and e.args[0] == 0:
                # This can happen when there is a lot of output and the user
                # sends a KeyboardInterrupt by pressing Control-C. E.g. in
                # a Python REPL when we execute "while True: print('test')".
                # (The `ptpython` REPL uses this `Output` class instead of
                # `stdout` directly -- in order to be network transparent.)
                # So, just ignore.
                pass
            else:
                raise

        self._buffer = []

    def ask_for_cpr(self):
        """
        Asks for a cursor position report (CPR).
        """
        self.write_raw('\x1b[6n')
        self.flush()

    def bell(self):
        " Sound bell. "
        self.write_raw('\a')
        self.flush()
