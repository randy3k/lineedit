from __future__ import unicode_literals

from collections import OrderedDict

from prompt_toolkit.auto_suggest import DynamicAutoSuggest
from prompt_toolkit.completion import DynamicCompleter, ThreadedCompleter
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding.key_bindings import DynamicKeyBindings, merge_key_bindings
from prompt_toolkit.validation import DynamicValidator

from prompt_toolkit.shortcuts.prompt import _true, CompleteStyle
from prompt_toolkit import PromptSession
from .buffer import ModalBuffer
from .history import ModalHistory, ModalInMemoryHistory, DynamicModalHistory


class Mode(object):
    key_bindings = None
    prompt_key_bindings = None

    def __init__(
            self,
            name,
            is_sticky=True,
            switchable_to=True,
            switchable_from=True,
            prompt_key_bindings=None,
            **kwargs):

        self.name = name
        self.is_sticky = is_sticky
        self.switchable_to = switchable_to
        self.switchable_from = switchable_from
        self.prompt_key_bindings = prompt_key_bindings
        if "key_bindings" in kwargs:
            self.key_bindings = kwargs["key_bindings"]
        self.kwargs = kwargs


def ensure_empty(kwargs, name):
    if name in kwargs and kwargs[name]:
        raise Exception("{} should not be set.".format(name))


class ModalPromptSession(PromptSession):
    _current_mode = None
    _key_bindings = None
    modes = OrderedDict()
    add_history = True
    before_accept = None

    def __init__(self, *args, **kwargs):
        self._check_args(kwargs)
        self._filter_args(kwargs)
        if "history" not in kwargs or not kwargs["history"]:
            kwargs["history"] = ModalInMemoryHistory()
        super(ModalPromptSession, self).__init__(*args, **kwargs)

    def _check_args(self, kwargs):
        ensure_empty(kwargs, "message")
        ensure_empty(kwargs, "default")
        ensure_empty(kwargs, "key_bindings")
        if "history" in kwargs:
            assert isinstance(kwargs["history"], ModalHistory)

    def _filter_args(self, kwargs):
        for key in (
                "add_history",
                "before_accept"):
            if key in kwargs:
                setattr(self, key, kwargs[key])
                del kwargs[key]

    def _create_default_buffer(self):
        """
        Create and return the default input buffer.
        """
        dyncond = self._dyncond

        # Create buffers list.
        def accept(buff):
            if self.before_accept:
                self.before_accept(buff)

            # remember the last working index
            buff.last_working_index = buff.working_index

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
            history=DynamicModalHistory(lambda: self.history),
            auto_suggest=DynamicAutoSuggest(lambda: self.auto_suggest),
            accept_handler=accept,
            get_tempfile_suffix=lambda: self.tempfile_suffix)

    def _create_application(self, *args, **kwargs):
        app = super(ModalPromptSession, self)._create_application(*args, **kwargs)
        app.session = self
        return app

    @property
    def current_mode_name(self):
        mode = self._current_mode
        if mode:
            return mode.name
        else:
            return None

    def change_mode(self, name, force=False, redraw=True):
        if name not in self.modes:
            raise Exception("no such mode")

        mode = self._current_mode
        newmode = self.modes[name]
        if mode and (mode.switchable_from or force):
            if newmode and (newmode.switchable_to or force):
                self.activate_mode(name)
                if redraw:
                    self.app._redraw()
                    self.app.layout.reset()
                    self.app.key_processor.reset()
                    self.app.vi_state.reset()

    @property
    def current_mode(self):
        return self._current_mode

    @property
    def main_mode(self):
        return next(iter(self.modes.values())) if len(self.modes) > 0 else None

    def register_mode(self, mode):
        assert isinstance(mode, Mode)
        self.modes[mode.name] = mode
        if len(self.modes) == 1:
            self.activate_mode(mode.name)

    def unregister_mode(self, name):
        del self.modes[name]

    def activate_mode(self, name):
        if name not in self.modes:
            return

        mode = self.modes[name]
        self._current_mode = mode

        for name in self._fields:
            if name is not "key_bindings":
                if name in mode.kwargs:
                    setattr(self, name, mode.kwargs[name])

        self.key_bindings = merge_key_bindings([
            DynamicKeyBindings(lambda: self.current_mode.prompt_key_bindings),
            merge_key_bindings([
                m.key_bindings for m in self.modes.values() if m.key_bindings
            ])
        ])

    def prompt(self, *args, **kwargs):
        self._check_args(kwargs)
        self._filter_args(kwargs)
        if args:
            raise Exception("positional arguments are deprecated")
        result = super(ModalPromptSession, self).prompt(**kwargs)

        # prompt will restore settings, we need to reactivate current mode
        if self.current_mode.is_sticky:
            self.activate_mode(self.current_mode_name)
        else:
            self.activate_mode(self.main_mode.name)

        return result
