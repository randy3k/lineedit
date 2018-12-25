class KeyPressEvent:
    def __init__(self, key_press):
        self.key_press = key_press


class KeyProcessor:
    def __init__(self, bind):
        self.bind = bind
        self._process = self._process_fsm()
        self._process.send(None)

    def call_handler(self, handler, kp):
        handler(KeyPressEvent(kp))

    def feed(self, data):
        if isinstance(data, list):
            for d in data:
                self._process.send(d)
        else:
            self._process.send(data)

    def _process_fsm(self):
        prefix = []
        while True:
            kp = yield
            prefix.append(kp)

            key = kp.key
            if isinstance(key, str) and ord(key) < 128:
                # ascii
                print(kp)

            elif self.bind.exact_match(key):
                self.call_handler(self.bind.get(key), kp)
                prefix = []

            # flush prefix
            prefix = []
