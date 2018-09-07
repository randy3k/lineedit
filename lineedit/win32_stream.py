from __future__ import unicode_literals

# derived from prompt_toolkit

from ctypes import windll, pointer
from ctypes.wintypes import DWORD, BOOL, HANDLE

from .win32_types import SECURITY_ATTRIBUTES, STD_INPUT_HANDLE, INPUT_RECORD, \
    KEY_EVENT_RECORD, EventTypes
from .key import Key, KeyEvent, ANSI_SEQUENCES, WIN32_KEYCODE

WAIT_TIMEOUT = 0x00000102
INFINITE = -1

LEFT_ALT_PRESSED = 0x0002
RIGHT_ALT_PRESSED = 0x0001
SHIFT_PRESSED = 0x0010
LEFT_CTRL_PRESSED = 0x0008
RIGHT_CTRL_PRESSED = 0x0004


class Win32Stream:
    def __init__(self, stdin=None):
        self.handle = windll.kernel32.GetStdHandle(STD_INPUT_HANDLE)

    def wait_until_ready(self, timeout=None):
        if timeout is None:
            timeout = INFINITE
        handles = [self.handle]
        arrtype = HANDLE * len(handles)
        handle_array = arrtype(*handles)

        ret = windll.kernel32.WaitForMultipleObjects(
            len(handle_array), handle_array, BOOL(False), DWORD(timeout))

        if ret == WAIT_TIMEOUT:
            return None
        else:
            h = handle_array[ret]
            return h

    def read(self):
        if not self.wait_until_ready(0):
            return

        return list(self._read_events())

    def _read_events(self):
        n = 2048
        nevents = DWORD(0)
        input_record = (INPUT_RECORD * n)()
        windll.kernel32.ReadConsoleInputW(
            self.handle, pointer(input_record), n, pointer(nevents))

        for i in range(nevents.value):
            ir = input_record[i]
            if ir.EventType in EventTypes:
                ev = getattr(ir.Event, EventTypes[ir.EventType])
                if type(ev) == KEY_EVENT_RECORD and ev.KeyDown:
                    for key in self._event_to_key(ev):
                        yield KeyEvent(key)

    def _event_to_key(self, ev):

        result = None

        u_char = ev.uChar.UnicodeChar
        if u_char == '\x00':
            if ev.VirtualKeyCode in WIN32_KEYCODE:
                result = WIN32_KEYCODE[ev.VirtualKeyCode]
        elif u_char in ANSI_SEQUENCES:
            # make windows 'Enter' vt100 compatiable
            if u_char == "\n" and ev.VirtualKeyCode == 13:
                u_char = "\r"
            result = ANSI_SEQUENCES[u_char]
        else:
            result = u_char

        # Correctly handle Control-Arrow keys.
        if (ev.ControlKeyState & LEFT_CTRL_PRESSED or
                ev.ControlKeyState & RIGHT_CTRL_PRESSED) and result:
            if result == Key.Left:
                result = Key.ControlLeft

            elif result == Key.Right:
                result = Key.ControlRight

            elif result == Key.Up:
                result = Key.ControlUp

            elif result == Key.Down:
                result = Key.ControlDown

        # Correctly handle Shift-Arrow keys.
        elif ev.ControlKeyState & SHIFT_PRESSED and result:
            if result == Key.Left:
                result = Key.ShiftLeft

            elif result == Key.Right:
                result = Key.ShiftRight

            elif result == Key.Up:
                result = Key.ShiftUp

            elif result == Key.Down:
                result = Key.ShiftDown

        if result == Key.Delete:
            if ev.ControlKeyState & SHIFT_PRESSED:
                result = Key.ShiftDelete
            elif ev.ControlKeyState & LEFT_CTRL_PRESSED or ev.ControlKeyState & RIGHT_CTRL_PRESSED:
                result = Key.ControlDelete

        # Turn 'Tab' into 'BackTab' when shift was pressed.
        if result == Key.ControlI and ev.ControlKeyState & SHIFT_PRESSED:
            result = Key.BackTab

        # Turn 'Space' into 'ControlAt' when control was pressed.
        if (ev.ControlKeyState & LEFT_CTRL_PRESSED or
                ev.ControlKeyState & RIGHT_CTRL_PRESSED) and result == ' ':
            result = Key.ControlAt

        if result:
            # Correctly handle Meta key.
            if ev.ControlKeyState & LEFT_ALT_PRESSED:
                return [Key.Escape, result]
            else:
                return [result]
        else:
            return []

    def raw_mode(self):
        return raw_mode()

    def cooked_mode(self):
        return cooked_mode()


def create_win32_event():
    """
    Creates a Win32 unnamed Event .

    http://msdn.microsoft.com/en-us/library/windows/desktop/ms682396(v=vs.85).aspx
    """
    return windll.kernel32.CreateEventA(
        pointer(SECURITY_ATTRIBUTES()),
        BOOL(True),  # Manual reset event.
        BOOL(False),  # Initial state.
        None  # Unnamed event object.
    )


class raw_mode(object):
    def __init__(self, fileno=None):
        self.handle = windll.kernel32.GetStdHandle(STD_INPUT_HANDLE)

    def __enter__(self):
        # Remember original mode.
        original_mode = DWORD()
        windll.kernel32.GetConsoleMode(self.handle, pointer(original_mode))
        self.original_mode = original_mode

        self._patch()

    def _patch(self):
        # Set raw
        ENABLE_ECHO_INPUT = 0x0004
        ENABLE_LINE_INPUT = 0x0002
        ENABLE_PROCESSED_INPUT = 0x0001

        windll.kernel32.SetConsoleMode(
            self.handle, self.original_mode.value &
            ~(ENABLE_ECHO_INPUT | ENABLE_LINE_INPUT | ENABLE_PROCESSED_INPUT))

    def __exit__(self, *a, **kw):
        # Restore original mode
        windll.kernel32.SetConsoleMode(self.handle, self.original_mode)


class cooked_mode(raw_mode):

    def _patch(self):
        # Set cooked.
        ENABLE_ECHO_INPUT = 0x0004
        ENABLE_LINE_INPUT = 0x0002
        ENABLE_PROCESSED_INPUT = 0x0001

        windll.kernel32.SetConsoleMode(
            self.handle, self.original_mode.value |
            (ENABLE_ECHO_INPUT | ENABLE_LINE_INPUT | ENABLE_PROCESSED_INPUT))
