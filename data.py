import sys
from dataclasses import dataclass, field, astuple, replace
import termios

from defines import STDIN_FILENO, STDOUT_FILENO, QUIT_TIMES

sys.dont_write_bytecode = True

# Helper functions
# This one can be replace by importing urses.ascii.iscntrl()

def iscntrl(char):
    if isinstance(char, str):
        val = int(ord(char)) 
    else:
        char = char.decode("utf-8") # In c we dont have to do this convertion.
        val = char
    return (0 <= val <= 31) or (val == 127)

#def iscntrl(char: bytes) -> bool: # We do this because we apply s.decode later so everything that comes here is a string.
#    if char in (b'\x1b[A', b'\x1b[B', b'\x1b[C', b'\x1b[D'):
#        return True
#    val = ord(char.decode("utf-8"))
#    return (0 <= val <= 31) or (val == 127)

def perror(s: str): # Python automatically halts the program when it encounters and error, so this function and all instances of it are useless unless with a try/excpet.
    _, exc_value, _ = sys.exc_info()
    if exc_value:
        print(f"{s}: {exc_value}", file=sys.stderr)
    else:
        print(s, file=sys.stderr)

def CTRL_KEY(k):
    return ord(k) & 0x1f

def realloc(b: bytearray, length: int) -> bytearray: # bytearray.resize()
    if len(b) == length:
        return b
    elif len(b) > length:
        return b[:length]
    elif len(b) < length:
        return b + bytearray(length)

# Structs
@dataclass
class TtyAttributes:
    iflag: int
    oflag: int
    cflag: int
    lflag: int
    ispeed: int
    ospeed: int
    cc: list[str | int] = field(default_factory=list)

@dataclass
class EditorSyntax:
    filetype: str
    flags: int
    singleline_comment_start: str
    multiline_comment_start: str
    multiline_comment_end: str
    filematch: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)

@dataclass
class Erow:
    idx: int
    size: int
    rsize: int
    chars: str
    render: str
    hl_open_comment: int
    hl: list[int] = field(default_factory=list)

@dataclass
class EditConfig:
    orig_termios: TtyAttributes
    syntax: EditorSyntax | None = None
    row: list[Erow] = field(default_factory=list)
    cx: int = 0
    cy: int = 0
    rx: int = 0
    rowoff: int = 0
    coloff: int = 0
    screenrows: int = 0
    screencols: int = 0
    numrows: int = 0
    dirty: bool = False
    quit_times: int = QUIT_TIMES
    filename: str = ""
    statusmsg: str = '\0'
    statusmsg_time: int = 0

@dataclass
class Winsize:
    ws_rows: int
    ws_col: int
    ws_xpixel: int
    ws_ypixel: int

E = EditConfig(orig_termios=TtyAttributes(*termios.tcgetattr(STDIN_FILENO)), syntax=None)
