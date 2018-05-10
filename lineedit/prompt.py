from __future__ import unicode_literals

from prompt_toolkit.auto_suggest import DynamicAutoSuggest
from prompt_toolkit.completion import DynamicCompleter, ThreadedCompleter
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.filters import Condition
from prompt_toolkit.history import DynamicHistory
from prompt_toolkit.validation import DynamicValidator

from prompt_toolkit.shortcuts.prompt import _true, CompleteStyle
from prompt_toolkit import PromptSession
from .buffer import ModalBuffer


def force_arg(kwargs, name, value):
    if name in kwargs:
        raise Exception("{} should not be set.".format(name))
    else:
        kwargs[name] = True


class ModalPromptSession(PromptSession):

    def __init__(self, *args, **kwargs):
        super(ModalPromptSession, self).__init__(*args, **kwargs)

    def _create_default_buffer(self):
        """
        Create and return the default input buffer.
        """
        dyncond = self._dyncond

        # Create buffers list.
        def accept(buff):
            """ Accept the content of the default buffer. This is called when
            the validation succeeds. """
            self.app.exit(result=buff.document.text)

            # Reset content before running again.
            self.app.pre_run_callables.append(buff.reset)

        return ModalBuffer(
            name=DEFAULT_BUFFER,
                # Make sure that complete_while_typing is disabled when
                # enable_history_search is enabled. (First convert to Filter,
                # to avoid doing bitwise operations on bool objects.)
            complete_while_typing=Condition(lambda:
                _true(self.complete_while_typing) and not
                self.complete_style == CompleteStyle.READLINE_LIKE),
            validate_while_typing=dyncond('validate_while_typing'),
            enable_history_search=dyncond('enable_history_search'),
            validator=DynamicValidator(lambda: self.validator),
            completer=DynamicCompleter(lambda:
                ThreadedCompleter(self.completer)
                if self.complete_in_thread and self.completer
                else self.completer),
            history=DynamicHistory(lambda: self.history),
            auto_suggest=DynamicAutoSuggest(lambda: self.auto_suggest),
            accept_handler=accept,
            get_tempfile_suffix=lambda: self.tempfile_suffix)
