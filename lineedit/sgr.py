from functools import lru_cache
from collections import namedtuple

Attrs = namedtuple(
    'Attrs', 'fgcolor bgcolor bold underline italic blink reverse hidden')


@lru_cache(maxsize=None)
def select_graphic_rendition(attrs):

    pass
