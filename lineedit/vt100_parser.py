from .key import Key, is_ansi_prefix, get_ansi_key


class Vt100Parser:
    def __init__(self, callback):
        self._paste_mode = False
        self._paste_data = ""
        self._parser = self._parser_fsm()
        self._parser.send(None)
        self._callback = callback

    def feed(self, data):
        if self._paste_mode:
            self._feed_bpm(data)
        else:
            for i, c in enumerate(data):
                if self._paste_mode:
                    self._feed_bpm(data[i:])
                    break
                else:
                    self._parser.send(c)

    def _feed_bpm(self, data):
        end_mark = '\x1b[201~'
        if end_mark in data:
            end_index = data.index(end_mark)
            self._paste_data += data[:end_index]
            self._callback(Key.BracketedPaste, self._paste_data)
            self._paste_data = ""
            self.feed(data[end_index + len(end_mark):])
            self._paste_mode = False
        else:
            self._paste_data += data

    def _parser_fsm(self):
        prefix = ""
        retry = False
        while True:
            if retry:
                retry = False
            else:
                char = yield
                prefix += char

            is_prefix = is_ansi_prefix(prefix)
            if is_prefix:
                continue

            key = get_ansi_key(prefix)
            if key:
                if key is Key.BracketedPaste:
                    self._paste_mode = True
                    prefix = ""
                    continue
                else:
                    self._callback(key)
                    prefix = ""
                    continue

            found = -1
            for i in range(len(prefix), 0, -1):
                key = get_ansi_key(prefix[:i])
                if key:
                    self._callback(key)
                    found = i
                    break

            if found >= 0:
                prefix = prefix[found:]
                if prefix:
                    retry = True
                continue

            self._callback(prefix[0])
            prefix = prefix[1:]
            if prefix:
                retry = True
