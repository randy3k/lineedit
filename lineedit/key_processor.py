from .current import current_buffer


class KeyPressEvent:
    def __init__(self, key_presses):
        if not isinstance(key_presses, list):
            key_presses = [key_presses]
        self.key_presses = key_presses
        self.buffer = current_buffer()

    @property
    def keys(self):
        return tuple(kp.key for kp in self.key_presses)

    @property
    def data(self):
        return [kp.data for kp in self.key_presses]


class KeyProcessor:
    def __init__(self, bindings):
        self.bindings = bindings
        self._process = self._process_fsm()
        self._process.send(None)

    def feed(self, data):
        if isinstance(data, list):
            for d in data:
                self._process.send(d)
        else:
            self._process.send(data)

    def _process_fsm(self):
        prefix = []
        retry = False
        while True:
            if retry:
                retry = False
            else:
                key_press = yield
                prefix.append(key_press)

            keys = tuple(kp.key for kp in prefix)
            if self.bindings.any_prefix(keys):
                continue

            matches = self.bindings.get_matches(keys)
            if matches:
                match = matches[-1]
                match.dispatch(KeyPressEvent(prefix))
                # flush prefix
                prefix = []
                continue

            found = -1
            for i in range(len(prefix), 0, -1):
                prefix_keys = tuple(kp.key for kp in prefix[:i])
                matches = self.bindings.get_matches(prefix_keys)
                if matches:
                    match = matches[-1]
                    match.dispatch(KeyPressEvent(prefix))
                    found = i

            if found >= 0:
                prefix = prefix[found:]
                if prefix:
                    retry = True
                continue

            matches = self.bindings.get_matches(keys[0])
            bind = None
            if matches:
                bind = matches[-1]
            else:
                matches = self.bindings.get_matches('<any>')
                if matches:
                    bind = matches[-1]
            if bind:
                bind.dispatch(KeyPressEvent(prefix[0]))

            prefix = prefix[1:]
            if prefix:
                retry = True
