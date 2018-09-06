from __future__ import unicode_literals
from enum import Enum


class Key(Enum):
    Escape = 'escape'

    Up = 'up'
    Down = 'down'
    Right = 'right'
    Left = 'left'

    Home = 'home'
    End = 'end'
    Delete = 'delete'
    ControlDelete = 'c-delete'
    PageUp = 'pageup'
    PageDown = 'pagedown'
    Insert = 'insert'

    ControlAt = 'c-@'
    ControlA = 'c-a'
    ControlB = 'c-b'
    ControlC = 'c-c'
    ControlD = 'c-d'
    ControlE = 'c-e'
    ControlF = 'c-f'
    ControlG = 'c-g'
    ControlH = 'c-h'
    ControlI = 'c-i'  # tab
    ControlJ = 'c-j'  # newline
    ControlK = 'c-k'
    ControlL = 'c-l'
    ControlM = 'c-m'  # cr
    ControlN = 'c-n'
    ControlO = 'c-o'
    ControlP = 'c-p'
    ControlQ = 'c-q'
    ControlR = 'c-r'
    ControlS = 'c-s'
    ControlT = 'c-t'
    ControlU = 'c-u'
    ControlV = 'c-v'
    ControlW = 'c-w'
    ControlX = 'c-x'
    ControlY = 'c-y'
    ControlZ = 'c-z'

    ControlBackslash = 'c-\\'
    ControlSquareClose = 'c-]'
    ControlCircumflex = 'c-^'
    ControlUnderscore = 'c-_'

    ControlLeft = 'c-left'
    ControlRight = 'c-right'
    ControlUp = 'c-up'
    ControlDown = 'c-down'

    ShiftLeft = 's-left'
    ShiftUp = 's-up'
    ShiftDown = 's-down'
    ShiftRight = 's-right'
    ShiftDelete = 's-delete'
    BackTab = 's-tab'

    F1 = 'f1'
    F2 = 'f2'
    F3 = 'f3'
    F4 = 'f4'
    F5 = 'f5'
    F6 = 'f6'
    F7 = 'f7'
    F8 = 'f8'
    F9 = 'f9'
    F10 = 'f10'
    F11 = 'f11'
    F12 = 'f12'
    F13 = 'f13'
    F14 = 'f14'
    F15 = 'f15'
    F16 = 'f16'
    F17 = 'f17'
    F18 = 'f18'
    F19 = 'f19'
    F20 = 'f20'
    F21 = 'f21'
    F22 = 'f22'
    F23 = 'f23'
    F24 = 'f24'

    ScrollUp = '<scroll-up>'
    ScrollDown = '<scroll-down>'

    CPRResponse = '<cursor-position-response>'
    Vt100MouseEvent = '<vt100-mouse-event>'
    WindowsMouseEvent = '<windows-mouse-event>'
    BracketedPaste = '<bracketed-paste>'

    Ignore = '<ignore>'


ANSI_SEQUENCES = {
    '\x00': Key.ControlAt,
    '\x01': Key.ControlA,
    '\x02': Key.ControlB,
    '\x03': Key.ControlC,
    '\x04': Key.ControlD,
    '\x05': Key.ControlE,
    '\x06': Key.ControlF,
    '\x07': Key.ControlG,
    '\x08': Key.ControlH,
    '\x09': Key.ControlI,
    '\x0a': Key.ControlJ,
    '\x0b': Key.ControlK,
    '\x0c': Key.ControlL,
    '\x0d': Key.ControlM,
    '\x0e': Key.ControlN,
    '\x0f': Key.ControlO,
    '\x10': Key.ControlP,
    '\x11': Key.ControlQ,
    '\x12': Key.ControlR,
    '\x13': Key.ControlS,
    '\x14': Key.ControlT,
    '\x15': Key.ControlU,
    '\x16': Key.ControlV,
    '\x17': Key.ControlW,
    '\x18': Key.ControlX,
    '\x19': Key.ControlY,
    '\x1a': Key.ControlZ,

    '\x1b': Key.Escape,
    '\x1c': Key.ControlBackslash,
    '\x1d': Key.ControlSquareClose,
    '\x1e': Key.ControlCircumflex,
    '\x1f': Key.ControlUnderscore,
    '\x7f': Key.ControlH
}


POSIX_SEQUENCES = ANSI_SEQUENCES.copy()
POSIX_SEQUENCES.update({
    '\x1b[A': Key.Up,
    '\x1b[B': Key.Down,
    '\x1b[C': Key.Right,
    '\x1b[D': Key.Left,
    '\x1b[H': Key.Home,
    '\x1bOH': Key.Home,
    '\x1b[F': Key.End,
    '\x1bOF': Key.End,
    '\x1b[3~': Key.Delete,
    '\x1b[3;2~': Key.ShiftDelete,
    '\x1b[3;5~': Key.ControlDelete,
    '\x1b[1~': Key.Home,
    '\x1b[4~': Key.End,
    '\x1b[5~': Key.PageUp,
    '\x1b[6~': Key.PageDown,
    '\x1b[7~': Key.Home,
    '\x1b[8~': Key.End,
    '\x1b[Z': Key.BackTab,
    '\x1b[2~': Key.Insert,

    '\x1bOP': Key.F1,
    '\x1bOQ': Key.F2,
    '\x1bOR': Key.F3,
    '\x1bOS': Key.F4,
    '\x1b[[A': Key.F1,
    '\x1b[[B': Key.F2,
    '\x1b[[C': Key.F3,
    '\x1b[[D': Key.F4,
    '\x1b[[E': Key.F5,
    '\x1b[11~': Key.F1,
    '\x1b[12~': Key.F2,
    '\x1b[13~': Key.F3,
    '\x1b[14~': Key.F4,
    '\x1b[15~': Key.F5,
    '\x1b[17~': Key.F6,
    '\x1b[18~': Key.F7,
    '\x1b[19~': Key.F8,
    '\x1b[20~': Key.F9,
    '\x1b[21~': Key.F10,
    '\x1b[23~': Key.F11,
    '\x1b[24~': Key.F12,
    '\x1b[25~': Key.F13,
    '\x1b[26~': Key.F14,
    '\x1b[28~': Key.F15,
    '\x1b[29~': Key.F16,
    '\x1b[31~': Key.F17,
    '\x1b[32~': Key.F18,
    '\x1b[33~': Key.F19,
    '\x1b[34~': Key.F20,

    # Xterm
    '\x1b[1;2P': Key.F13,
    '\x1b[1;2Q': Key.F14,
    # '\x1b[1;2R': Key.F15,  # Conflicts with CPR response.
    '\x1b[1;2S': Key.F16,
    '\x1b[15;2~': Key.F17,
    '\x1b[17;2~': Key.F18,
    '\x1b[18;2~': Key.F19,
    '\x1b[19;2~': Key.F20,
    '\x1b[20;2~': Key.F21,
    '\x1b[21;2~': Key.F22,
    '\x1b[23;2~': Key.F23,
    '\x1b[24;2~': Key.F24,

    '\x1b[1;5A': Key.ControlUp,
    '\x1b[1;5B': Key.ControlDown,
    '\x1b[1;5C': Key.ControlRight,
    '\x1b[1;5D': Key.ControlLeft,

    '\x1b[1;2A': Key.ShiftUp,
    '\x1b[1;2B': Key.ShiftDown,
    '\x1b[1;2C': Key.ShiftRight,
    '\x1b[1;2D': Key.ShiftLeft,

    '\x1bOA': Key.Up,
    '\x1bOB': Key.Down,
    '\x1bOC': Key.Right,
    '\x1bOD': Key.Left,

    '\x1b[5A': Key.ControlUp,
    '\x1b[5B': Key.ControlDown,
    '\x1b[5C': Key.ControlRight,
    '\x1b[5D': Key.ControlLeft,

    '\x1bOc': Key.ControlRight,
    '\x1bOd': Key.ControlLeft,

    # Tmux (Win32 subsystem) sends the following scroll events. Ignored for now.
    '\x1b[62~': Key.ScrollUp,
    '\x1b[63~': Key.ScrollDown,

    '\x1b[200~': Key.BracketedPaste,  # Start of bracketed paste.

    '\x1b[1;3D': (Key.Escape, Key.Left),
    '\x1b[1;3C': (Key.Escape, Key.Right),
    '\x1b[1;3A': (Key.Escape, Key.Up),
    '\x1b[1;3B': (Key.Escape, Key.Down),
    '\x1b[1;9D': (Key.Escape, Key.Left),
    '\x1b[1;9C': (Key.Escape, Key.Right),

    '\x1b[E': Key.Ignore,
    '\x1b[G': Key.Ignore
})


WIN32_KEYCODE = {
    33: Key.PageUp,
    34: Key.PageDown,
    35: Key.End,
    36: Key.Home,

    # Arrows
    37: Key.Left,
    38: Key.Up,
    39: Key.Right,
    40: Key.Down,

    45: Key.Insert,
    46: Key.Delete,

    # F-keys.
    112: Key.F1,
    113: Key.F2,
    114: Key.F3,
    115: Key.F4,
    116: Key.F5,
    117: Key.F6,
    118: Key.F7,
    119: Key.F8,
    120: Key.F9,
    121: Key.F10,
    122: Key.F11,
    123: Key.F12
}


class IS_POSIX_SEQUENCES_PREFIX(dict):
    """
    Use a dict to cache prefix result
    """
    def __missing__(self, prefix):
        is_prefix = any(v for k, v in POSIX_SEQUENCES.items() if k.startswith(prefix) and k != prefix)
        self[prefix] = is_prefix
        return is_prefix


_is_posix_sequences_prefix = IS_POSIX_SEQUENCES_PREFIX()


def is_posix_prefix(s):
    return _is_posix_sequences_prefix[s]


def get_posix_key(s):
    try:
        return POSIX_SEQUENCES[s]
    except KeyError:
        return None
