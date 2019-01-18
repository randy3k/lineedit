def get_command(name):
    if name in globals():
        return globals()[name]
    elif name.replace('-', '_') in globals():
        return globals()[name.replace('-', '_')]

    raise KeyError('readline command not found: {}'.format(name))


# Commands For Moving

def beginning_of_line(event):
    event.buffer.document.move_cursor_to_bol()


def end_of_line(event):
    event.buffer.document.move_cursor_to_eol()


def forward_char(event):
    raise NotImplementedError()


def backward_char(event):
    raise NotImplementedError()


def forward_word(event):
    raise NotImplementedError()


def backward_word(event):
    raise NotImplementedError()


def previous_screen_line(event):
    raise NotImplementedError()


def next_screen_line(event):
    raise NotImplementedError()


def clear_screen(event):
    raise NotImplementedError()


def redraw_current_line(event):
    raise NotImplementedError()


# Commands For Manipulating The History

def accept_line(event):
    raise NotImplementedError()


def previous_history(event):
    raise NotImplementedError()


def next_history(event):
    raise NotImplementedError()


def beginning_of_history(event):
    raise NotImplementedError()


def end_of_history(event):
    raise NotImplementedError()


def reverse_search_history(event):
    raise NotImplementedError()


def forward_search_history(event):
    raise NotImplementedError()


def non_incremental_reverse_search_history(event):
    raise NotImplementedError()


def non_incremental_forward_search_history(event):
    raise NotImplementedError()


def history_search_forward(event):
    raise NotImplementedError()


def history_search_backward(event):
    raise NotImplementedError()


def history_substring_search_forward(event):
    raise NotImplementedError()


def history_substring_search_backward(event):
    raise NotImplementedError()


def yank_nth_arg(event):
    raise NotImplementedError()


def yank_last_arg(event):
    raise NotImplementedError()


# Commands For Changing Text

def end_of_file(event):
    raise NotImplementedError()


def delete_char(event):
    raise NotImplementedError()


def backward_delete_char(event):
    raise NotImplementedError()


def forward_backward_delete_char(event):
    raise NotImplementedError()


def quoted_insert(event):
    raise NotImplementedError()


def tab_insert(event):
    raise NotImplementedError()


def self_insert(event):
    for key in event.keys:
        if isinstance(key, str) and ord(key) < 128:
            event.buffer.insert_text(key)


def bracketed_paste_begin(event):
    raise NotImplementedError()


def transpose_chars(event):
    raise NotImplementedError()


def transpose_words(event):
    raise NotImplementedError()


def upcase_word(event):
    raise NotImplementedError()


def downcase_word(event):
    raise NotImplementedError()


def capitalize_word(event):
    raise NotImplementedError()


def overwrite_mode(event):
    raise NotImplementedError()


# Killing And Yanking


def kill_line(event):
    raise NotImplementedError()


def backward_kill_line(event):
    raise NotImplementedError()


def unix_line_discard(event):
    raise NotImplementedError()


def kill_whole_line(event):
    raise NotImplementedError()


def kill_word(event):
    raise NotImplementedError()


def backward_kill_word(event):
    raise NotImplementedError()


def unix_word_rubout(event):
    raise NotImplementedError()


def unix_filename_rubout(event):
    raise NotImplementedError()


def delete_horizontal_space(event):
    raise NotImplementedError()


def kill_region(event):
    raise NotImplementedError()


def copy_region_as_kill(event):
    raise NotImplementedError()


def copy_backward_word(event):
    raise NotImplementedError()


def copy_forward_word(event):
    raise NotImplementedError()


def yank(event):
    raise NotImplementedError()


def yank_pop(event):
    raise NotImplementedError()


# Letting Readline Type For You

def possible_completions(event):
    raise NotImplementedError()


def insert_completions(event):
    raise NotImplementedError()


def menu_complete(event):
    raise NotImplementedError()


def menu_complete_backward(event):
    raise NotImplementedError()


def delete_char_or_list(event):
    raise NotImplementedError()


def complete_filename(event):
    raise NotImplementedError()


def possible_filename_completions(event):
    raise NotImplementedError()


def complete_username(event):
    raise NotImplementedError()


def possible_username_completions(event):
    raise NotImplementedError()


def complete_variable(event):
    raise NotImplementedError()


def possible_variable_completions(event):
    raise NotImplementedError()


def complete_hostname(event):
    raise NotImplementedError()


def possible_hostname_completions(event):
    raise NotImplementedError()


def complete_command(event):
    raise NotImplementedError()


def possible_command_completions(event):
    raise NotImplementedError()


def dynamic_complete_history(event):
    raise NotImplementedError()


def dabbrev_expand(event):
    raise NotImplementedError()


def complete_into_braces(event):
    raise NotImplementedError()


# Some Miscellaneous Commands

def re_read_init_file(event):
    raise NotImplementedError()


def abort(event):
    raise NotImplementedError()


def do_lowercase_version(event):
    raise NotImplementedError()


def undo(event):
    raise NotImplementedError()


def revert_line(event):
    raise NotImplementedError()


def tilde_expand(event):
    raise NotImplementedError()


def set_mark(event):
    raise NotImplementedError()


def exchange_point_and_mark(event):
    raise NotImplementedError()


def character_search(event):
    raise NotImplementedError()


def character_search_backward(event):
    raise NotImplementedError()


def skip_csi_sequence(event):
    raise NotImplementedError()


def insert_comment(event):
    raise NotImplementedError()


def dump_functions(event):
    raise NotImplementedError()


def dump_variables(event):
    raise NotImplementedError()


def dump_macros(event):
    raise NotImplementedError()


def glob_complete_word(event):
    raise NotImplementedError()


def glob_expand_word(event):
    raise NotImplementedError()


def glob_list_expansions(event):
    raise NotImplementedError()


def display_shell_version(event):
    raise NotImplementedError()


def shell_expand_line(event):
    raise NotImplementedError()


def history_expand_line(event):
    raise NotImplementedError()


def magic_space(event):
    raise NotImplementedError()


def alias_expand_line(event):
    raise NotImplementedError()


def history_and_alias_expand_line(event):
    raise NotImplementedError()


def insert_last_argument(event):
    raise NotImplementedError()


def operate_and_get_next(event):
    raise NotImplementedError()


def edit_and_execute_command(event):
    raise NotImplementedError()
