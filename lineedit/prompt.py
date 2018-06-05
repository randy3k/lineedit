from __future__ import unicode_literals

from collections import OrderedDict
from six import text_type

from prompt_toolkit.auto_suggest import DynamicAutoSuggest
from prompt_toolkit.completion import DynamicCompleter, ThreadedCompleter
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding.key_bindings import DynamicKeyBindings, merge_key_bindings
from prompt_toolkit.validation import DynamicValidator

from prompt_toolkit.shortcuts.prompt import _true, CompleteStyle
from prompt_toolkit import PromptSession
from .buffer import ModalBuffer
from .history import ModalHistory, ModalInMemoryHistory


class Mode(object):
    def __init__(
            self,
            name,
            on_activated=None,
            on_pre_accept=None,
            on_dectivated=None,
            keep_history=True,
            history_share_with=False,
            switchable_to=True,
            switchable_from=True,
            key_bindings=None,
            prompt_key_bindings=None,
            **kwargs):

        def _ensure_func(x):
            if isinstance(x, bool):
                return lambda m: x
            elif isinstance(x, list):
                return lambda m: m in x
            elif isinstance(x, text_type):
                return lambda m: m == x
            else:
                return x

        self.name = name
        self.on_activated = on_activated
        self.on_pre_accept = on_pre_accept
        self.on_dectivated = on_dectivated
        self.keep_history = keep_history
        self.history_share_with = _ensure_func(history_share_with)
        self.switchable_to = _ensure_func(switchable_to)
        self.switchable_from = _ensure_func(switchable_from)
        self.prompt_key_bindings = prompt_key_bindings
        self.key_bindings = key_bindings
        for key in kwargs:
            setattr(self, key, kwargs[key])


def ensure_empty(kwargs, name):
    if name in kwargs and kwargs[name]:
        raise Exception("{} should not be set.".format(name))


class ModalPromptSession(PromptSession):
    _current_mode = None
    _key_bindings = None
    _default_settings = {}
    modes = OrderedDict()
    mode_class = Mode

    # new settings
    add_history = True
    history_search_no_duplicates = False

    def __init__(self, *args, **kwargs):
        self._check_args(kwargs)
        self._filter_args(kwargs)
        if "history" not in kwargs or not kwargs["history"]:
            kwargs["history"] = ModalInMemoryHistory()
        super(ModalPromptSession, self).__init__(*args, **kwargs)
        self._backup_settings()

    def _check_args(self, kwargs):
        ensure_empty(kwargs, "message")
        ensure_empty(kwargs, "default")
        ensure_empty(kwargs, "key_bindings")
        if "history" in kwargs:
            assert isinstance(kwargs["history"], ModalHistory)

    def _filter_args(self, kwargs):
        for key in (
                "add_history",
                "history_search_no_duplicates",
                "mode_class"):
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
            if self.current_mode.on_pre_accept:
                self.current_mode.on_pre_accept(self)

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
            history=self.history,
            auto_suggest=DynamicAutoSuggest(lambda: self.auto_suggest),
            accept_handler=accept,
            tempfile_suffix=lambda: self.tempfile_suffix)

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

    @property
    def current_mode(self):
        return self._current_mode

    @property
    def main_mode(self):
        return next(iter(self.modes.values())) if len(self.modes) > 0 else None

    def register_mode(self, mode_or_name=None, **kwargs):
        if isinstance(mode_or_name, self.mode_class):
            mode = mode_or_name
        else:
            mode = self.mode_class(text_type(mode_or_name), **kwargs)
        self.modes[mode.name] = mode
        if len(self.modes) == 1:
            self.activate_mode(mode.name)
        else:
            self.activate_mode(self.current_mode_name, force=True)

    def unregister_mode(self, name):
        del self.modes[name]

    def change_mode(self, name, force=False):
        if name not in self.modes:
            raise Exception("no such mode")

        mode = self._current_mode
        newmode = self.modes[name]
        if not mode or not newmode:
            return

        if mode.name == newmode.name and not force:
            return

        if not mode.switchable_to or mode.switchable_to(newmode.name):
            if not newmode.switchable_from or newmode.switchable_from(mode.name):
                self.activate_mode(name, force)

    def activate_mode(self, name, force=False):
        if name not in self.modes:
            raise Exception("no such mode")

        mode = self.modes[name]

        if self.current_mode_name == mode.name and not force:
            return

        current_mode = self.current_mode
        if current_mode and current_mode.on_dectivated:
            current_mode.on_dectivated(self)

        self._current_mode = mode

        self._restore_settings()
        for name in self._fields:
            if name is not "key_bindings":
                if hasattr(mode, name):
                    setattr(self, name, getattr(mode, name))

        self.key_bindings = merge_key_bindings([
            DynamicKeyBindings(lambda: self.current_mode.prompt_key_bindings),
            merge_key_bindings([
                m.key_bindings for m in self.modes.values() if m.key_bindings
            ])
        ])

        if mode.on_activated:
            mode.on_activated(self)

    def _backup_settings(self):
        for name in self._fields:
            self._default_settings[name] = getattr(self, name)

    def _restore_settings(self):
        for name in self._fields:
            setattr(self, name, self._default_settings[name])

    def prompt(self, *args, **kwargs):
        self._check_args(kwargs)
        self._filter_args(kwargs)
        if args:
            raise Exception("positional arguments are deprecated")

        backup = self._default_settings.copy()
        for name in self._fields:
            if name in kwargs:
                value = kwargs[name]
                if value is not None:
                    setattr(self._default_settings, name, value)

        orig_mode = self.current_mode_name
        try:
            result = super(ModalPromptSession, self).prompt(**kwargs)
        except KeyboardInterrupt:
            self._default_settings = backup.copy()
            self.activate_mode(orig_mode, force=True)
            raise KeyboardInterrupt
        finally:
            self._default_settings = backup.copy()

        # prompt will restore settings, we need to reactivate current mode
        self.activate_mode(self.current_mode_name, force=True)
        return result
