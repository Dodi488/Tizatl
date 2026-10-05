import os
import sys
from dataclasses import dataclass, field, astuple, replace
import termios
import atexit
import errno
import fcntl
import array
#import tuple

from data import *

sys.dont_write_bytecode = True

def die(s: str) -> None:
    os.write(STDOUT_FILENO, b'\x1b[2J'[:4])
    os.write(STDOUT_FILENO, b'\x1b[H'[:3])

    perror(s)
    sys.exit(1)

def disable_raw_mode() -> None:
    try:
        termios.tcsetattr(STDIN_FILENO, termios.TCSAFLUSH, list(astuple(E.orig_termios)))
    except termios.error:
        die("tcsetattr")

def enable_raw_mode() -> None:
    try:
        E.orig_termios = TtyAttributes(*termios.tcgetattr(STDIN_FILENO))
    except termios.error:
        die("tcgetattr")

    atexit.register(disable_raw_mode)

    raw = replace(E.orig_termios)
    raw.iflag &= ~(termios.BRKINT | termios.ICRNL | termios.INPCK | termios.ISTRIP | termios.IXON)
    raw.oflag &= ~(termios.OPOST)
    raw.cflag |= (termios.CS8)
    raw.lflag &= ~(termios.ECHO | termios.ICANON | termios.IEXTEN | termios.ISIG)
    raw.cc[termios.VMIN] = 0
    raw.cc[termios.VTIME] = 1

    try:
        termios.tcsetattr(STDIN_FILENO, termios.TCSAFLUSH, list(astuple(raw)))
    except termios.error:
        die("tcsetattr")
    # The proble with this code is that Python does not actually set values with pointers like c does, we are just creating a local copy and modifying it.
    # We are going to define a class and alter its values.

def editor_read_key() -> bytes:
    while True:
        try:
            c = os.read(STDIN_FILENO, 1)
            if c:
                break
        except OSError as e:
            if e.errno != errno.EAGAIN:
                die("read")

    if (c == b'\x1b'):
        seq = [b'0'] * 3

        try:
            seq[0] = os.read(STDIN_FILENO, 1)
        except OSError:
            return b'\x1b'

        try:
            seq[1] = os.read(STDIN_FILENO, 1)
        except OSError:
            return b'\x1b'

        if seq[0] == b'[':
            if seq[1] >= b'0' and seq[1] <= b'9':
                try:
                    seq[2] = os.read(STDIN_FILENO, 1)
                except OSError:
                    return b'\x1b'
                if seq[2] == b'~':
                    match seq[1]:
                        case b'1': return EditorKey.HOME_KEY.value
                        case b'3': return EditorKey.DEL_KEY.value
                        case b'4': return EditorKey.END_KEY.value
                        case b'5': return EditorKey.PAGE_UP.value
                        case b'6': return EditorKey.PAGE_DOWN.value
                        case b'7': return EditorKey.HOME_KEY.value
                        case b'8': return EditorKey.END_KEY.value
            else:
                match seq[1]:
                    case b'A': return EditorKey.MOVE_UP.value
                    case b'B': return EditorKey.MOVE_DOWN.value
                    case b'C': return EditorKey.MOVE_RIGHT.value
                    case b'D': return EditorKey.MOVE_LEFT.value
                    case b'H': return EditorKey.HOME_KEY.value
                    case b'F': return EditorKey.END_KEY.value
                    case _: return b'\x1b'

        elif seq[0] == b'O':
            match seq[1]:
                case b'H': return EditorKey.HOME_KEY.value
                case b'F': return EditorKey.END_KEY.value

    return c

def get_cursor_position() -> tuple(int, int):
    buf = [b'\x00'] * 32
    i = 0

    if os.write(STDOUT_FILENO, b'\x1b[6n'[:4]) != 4:
        return -1, -1

    while (i < (len(buf) - 1)):
        c = os.read(STDIN_FILENO, 1)

        if not c:
            break

        if c == b'R':
            break

        buf[i] = c
        i += 1

    buf[i] = b'\x00'

    if (buf[0] != b'\x1b' or buf[1] != b'['):
        return -1, -1

    buf = b''.join(buf[2:]).replace(b'\x00', b'').decode('ascii')
    sizes = buf.split(";")
    if len(sizes) != 2:
        return -1, -1
    else:
        return int(sizes[0]), int(sizes[1])

def get_window_size(config: EditorConfig) -> int: # This function can be errased with size = shutil.get_terminal_size()
    ws_bytes = array.array('H', [4, 4, 4, 4])

    try:
        fcntl.ioctl(STDOUT_FILENO, termios.TIOCGWINSZ, ws_bytes)
        ws = Winsize(*ws_bytes)

        if ws.ws_col == 0:
            raise OSError

    except:
        if ((c := os.write(STDOUT_FILENO, b'\x1b[999C\x1b[999B'[:12])) != 12):
            return -1

        if ws.ws_col == 0:
            return -1

        position = get_cursor_position()
        if position == (-1, -1):
            return -1

        config.screenrows, config.screencols = position
        return 0

    config.screencols = ws.ws_col
    config.screenrows = ws.ws_rows
