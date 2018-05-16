from __future__ import unicode_literals
import datetime
import os
from prompt_toolkit.history import History


class ModalHistory(History):
    _loaded_strings = []
    _loaded_modes = []

    def start_loading(self):
        pass

    def load_history_strings(self):
        pass

    def get_modes(self):
        return self._loaded_modes

    def last_string(self):
        return self._loaded_strings[-1]

    def last_mode(self):
        return self._loaded_modes[-1]

    def size(self):
        # we cannot introduce __len__ because prompt has a sentence of
        # `history or InMemoryHistory()`

        return len(self._loaded_modes)


class ModalInMemoryHistory(ModalHistory):

    def __init__(self, include_modes=None, exclude_modes=[]):
        self.include_modes = include_modes
        self.exclude_modes = exclude_modes
        super(ModalInMemoryHistory, self).__init__()

    def get_modes(self):
        return self._loaded_modes

    def append_string(self, string, mode):
        if not mode:
            return

        # don't append to history if this mode is excluced
        if mode in self.exclude_modes:
            return
        # don't append to history if this mode is not included
        if self.include_modes and mode not in self.include_modes:
            return

        self._loaded_strings.append(string)
        self._loaded_modes.append(mode)

    def store_string(self, string, mode):
        pass


class ModalFileHistory(ModalHistory):

    def __init__(self, filename, include_modes=None, exclude_modes=[]):
        self.filename = filename
        self.include_modes = include_modes
        self.exclude_modes = exclude_modes
        super(ModalFileHistory, self).__init__()

    def start_loading(self):
        lines = []
        mode = [None]

        def add():
            if lines:
                # Join and drop trailing newline.
                string = ''.join(lines)[:-1]

                self._loaded_strings.append(string)
                self._loaded_modes.append(mode[0])

        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as f:
                for line in f:
                    line = line.decode('utf-8')

                    if line.startswith('# mode: '):
                        mode[0] = line.replace('# mode: ', '').strip()
                    elif line.startswith('+'):
                        lines.append(line[1:])
                    else:
                        add()
                        mode = [None]
                        lines = []

                add()

    def append_string(self, string, mode):
        if not mode:
            return

        # don't append to history if this mode is excluced
        if mode in self.exclude_modes:
            return
        # don't append to history if this mode is not included
        if self.include_modes and mode not in self.include_modes:
            return

        self._loaded_strings.append(string)
        self._loaded_modes.append(mode)
        self.store_string(string, mode)

    def store_string(self, string, mode):
        # Save to file.
        with open(self.filename, 'ab') as f:
            def write(t):
                f.write(t.encode('utf-8'))

            write('\n# time: %s UTC' % datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
            write('\n# mode: %s\n' % mode)
            for line in string.split('\n'):
                write('+%s\n' % line)
