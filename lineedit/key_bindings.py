from collections import OrderedDict
from .readline import get_command
from .key import Key


def _Key(key):
    try:
        return Key(key)
    except ValueError:
        return key


def normalize_keys(keys):
    if isinstance(keys, tuple):
        keys = tuple(_Key(k) for k in keys)
    else:
        keys = _Key(keys)
    return keys


class Bind:
    def __init__(self, keys, callback, conditions=[]):
        self.keys = normalize_keys(keys)
        self.callback = callback
        if not isinstance(conditions, list):
            conditions = [conditions]
        self.conditions = conditions

    def enabled(self):
        if not self.conditions:
            return True

        for con in self.conditions:
            if not con():
                return False
        return True

    def dispatch(self, event):
        # with open("/tmp/lineedit", "a") as f:
        #     f.write(str(event.keys))
        #     f.write("\n")
        self.callback(event)


class KeyBindings:
    _binds = OrderedDict()

    def _add(self, keys, callback, conditions=[]):
        keys = normalize_keys(keys)
        if keys not in self._binds:
            self._binds[keys] = []
        self._binds[keys].append(Bind(keys, callback, conditions))

    def add(self, keys, conditions=[]):
        def adder(callback):
            self._add(keys, callback, conditions)

        return adder

    def _get_matches(self, keys):
        """
        It is not safe.
        """
        for bind in self._binds[keys]:
            if bind.enabled():
                yield bind

    def get_matches(self, keys):
        keys = normalize_keys(keys)
        if keys not in self._binds:
            return []

        return list(self._get_matches(keys))

    # def exact_match(self, keys):
    #     try:
    #         keys = self.normalize_keys(keys)
    #         for bind in self._binds[keys]:
    #             if bind.enabled():
    #                 return True
    #     except ValueError:
    #         return False

    def any_prefix(self, keys):
        keys = normalize_keys(keys)
        klen = len(keys)
        for k in self._binds:
            if isinstance(k, tuple) and klen < len(k):
                if k[:klen] == keys:
                    for bind in self._binds[k]:
                        if bind.enabled():
                            return True
        return False


def noop(event):
    pass


def default_bindings():
    bindings = KeyBindings()

    @bindings.add('left')
    def _(event):
        event.buffer.document.move_cursor_to_left()

    @bindings.add('right')
    def _(event):
        event.buffer.document.move_cursor_to_right()

    @bindings.add('up')
    def _(event):
        event.buffer.auto_up()

    @bindings.add('down')
    def _(event):
        event.buffer.auto_down()


    bindings.add('c-a')(get_command('beginning-of-line'))
    bindings.add('c-e')(get_command('end-of-line'))
    bindings.add('c-d')(get_command('end-of-file'))
    bindings.add((Key.Escape, Key.Escape))(noop)
    bindings.add((Key.Escape, 'b'))(get_command('backward-word'))
    bindings.add((Key.Escape, 'f'))(get_command('forward-word'))

    @bindings.add((Key.Escape, 'c-m'))
    def _(event):
        event.buffer.insert_text('\n')

    bindings.add('<any>')(get_command('self-insert'))
    return bindings
