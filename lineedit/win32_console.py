from .vt100_console import Vt100Console
from .win32_types import STD_OUTPUT_HANDLE, CONSOLE_SCREEN_BUFFER_INFO
from ctypes.wintypes import DWORD
from ctypes import windll, byref


ENABLE_PROCESSED_INPUT = 0x0001
ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004


class Win32Console(Vt100Console):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hconsole = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    def get_screen_buffer_info(self):
        sbinfo = CONSOLE_SCREEN_BUFFER_INFO()
        windll.kernel32.GetConsoleScreenBufferInfo(self._hconsole, byref(sbinfo))
        return sbinfo

    def get_size(self):
        sbinfo = self.get_screen_buffer_info()
        height = sbinfo.srWindow.Bottom - sbinfo.srWindow.Top + 1
        width = sbinfo.dwSize.X
        return (height, width)

    def get_cursor_position(self):
        sbinfo = self.get_screen_buffer_info()
        return (sbinfo.dwCursorPosition.Y, sbinfo.dwCursorPosition.X)

    def flush(self):
        original_mode = DWORD(0)
        windll.kernel32.GetConsoleMode(self._hconsole, byref(original_mode))

        # Enable processing of vt100 sequences.
        windll.kernel32.SetConsoleMode(self._hconsole, DWORD(
            ENABLE_PROCESSED_INPUT | ENABLE_VIRTUAL_TERMINAL_PROCESSING))

        try:
            super().flush()
        finally:
            windll.kernel32.SetConsoleMode(self._hconsole, original_mode)
