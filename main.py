import sys

sys.dont_write_bytecode = True

from terminal import enable_raw_mode, get_window_size, die
from input import editor_process_keypress
from output import editor_refresh_screen, editor_set_status_message
from data import E
from file_io import editor_open

def init_editor() -> None:
    try:
        get_window_size(E)
    except OSError:
        die("get_window_error")

    E.screenrows -= 2

def main():
    enable_raw_mode()
    init_editor()
    if len(sys.argv) >= 2:
        editor_open(sys.argv[1])

    editor_set_status_message("HELP: Ctrl-S = save | Ctrl-Q = quit | Ctrl-F = find")

    while True:
        editor_refresh_screen()
        editor_process_keypress()

if __name__ == "__main__":
    main()
