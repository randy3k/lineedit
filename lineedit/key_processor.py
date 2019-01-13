from .current import current_buffer


class KeyPressEvent:
    def __init__(self, key_presses):
        self.key_presses = key_presses
        self._buffer = current_buffer()

    @property
    def keys(self):
        return [kp.key for kp in self.key_presses]

    @property
    def data(self):
        return [kp.data for kp in self.key_presses]

    @property
    def buffer(self):
        return self._buffer


def default_handler(event):
    for key in event.keys:
        event.buffer.insert_text(key)


class KeyProcessor:
    def __init__(self, bind):
        self.bind = bind
        self._process = self._process_fsm()
        self._process.send(None)

    def call_handler(self, handler, key_presses):
        handler(KeyPressEvent(key_presses))

    def feed(self, data):
        if isinstance(data, list):
            for d in data:
                self._process.send(d)
        else:
            self._process.send(data)

    def _process_fsm(self):
        # FIXME: handle prefix keys
        prefix = []
        while True:
            key_press = yield
            prefix.append(key_press)

            key = key_press.key
            if isinstance(key, str) and ord(key) < 128:
                # ascii
                self.call_handler(default_handler, [key_press])

            elif self.bind.exact_match(key):
                self.call_handler(self.bind.get(key), [key_press])
                prefix = []

            # flush prefix
            prefix = []
