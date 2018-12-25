from functools import lru_cache
from .key import Key


class KeyBindings:
    _registry = {}

    def normalize_key(sele, key):
        if isinstance(key, tuple):
            key = (Key(k) for k in key)
        else:
            key = Key(key)
        return key

    def _add(self, key, callback):
        if key not in self._registry:
            self._registry[key] = []
        self._registry[key].append(callback)

    def add(self, key):
        def adder(callback):
            self._add(self.normalize_key(key), callback)

        return adder

    def get(self, key):
        # get the active handler
        return self._registry[key][0]

    @lru_cache(maxsize=512)
    def exact_match(self, key):
        return self.normalize_key(key) in self._registry

    @lru_cache(maxsize=512)
    def any_prefix(self, key):
        klen = len(key)
        for rkey in self._registry:
            if isinstance(rkey, tuple) and klen < len(rkey):
                if rkey[:klen] == key:
                    return True
        return False
