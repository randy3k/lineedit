from .deps import dependencies_loaded
if not dependencies_loaded:
    print("Dependencies not loaded.")

from .prompt import Mode, ModalPromptSession  # noqa
from .history import ModalInMemoryHistory, ModalFileHistory  # noqa


__all__ = [
    "Mode",
    "ModalPromptSession",
    "ModalInMemoryHistory",
    "ModalFileHistory"
]


__version__ = "0.1.0"
