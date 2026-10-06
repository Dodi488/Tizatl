import sys
from dataclasses import dataclass, field, astuple, replace
import termios
from enum import Enum

sys.dont_write_bytecode = True

# Helper functions
# This one can be replace by importing urses.ascii.iscntrl()
#def iscntrl(char):
#    char = char.decode("utf-8") # In c we dont have to do this convertion.
#    if isinstance(char, str):
#        val = int(ord(char)) 
#    else:
#        val = char
#    return (0 <= val <= 31) or (val == 127)

def iscntrl(char: bytes) -> bool: # We do this because we apply s.decode later so everything that comes here is a string.
    val = ord(char.decode("utf-8"))
    return (0 <= val <= 31) or (val == 127)

def perror(s: str): # Python automatically halts the program when it encounters and error, so this function and all instances of it are useless unless with a try/excpet.
    _, exc_value, _ = sys.exc_info()
    if exc_value:
        print(f"{s}: {exc_value}", file=sys.stderr)
    else:
        print(s, file=sys.stderr)

def realloc(b: bytearray, length: int) -> bytearray: # bytearray.resize()
    if len(b) == length:
        return b
    elif len(b) > length:
        return b[:length]
    elif len(b) < length:
        return b + bytearray(length)

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
class Erow:
    size: int
    rsize: int
    chars: str
    #render: list[str] = field(default_factory=list)
    render: str

@dataclass
class EditConfig:
    orig_termios: TtyAttributes
    row: list[Erow] = field(default_factory=list)
    cx: int = 0
    cy: int = 0
    rx: int = 0
    rowoff: int = 0
    coloff: int = 0
    screenrows: int = 0
    screencols: int = 0
    numrows: int = 0
    filename: str = "New"
    statusmsg: str = '\0'
    statusmsg_time: int = 0

@dataclass
class Winsize:
    ws_rows: int
    ws_col: int
    ws_xpixel: int
    ws_ypixel: int

STDIN_FILENO = sys.stdin.fileno()
STDOUT_FILENO = sys.stdout.fileno()
TIZATL_VERSION = "0.0.1"
TAB_STOP_SIZE = 4

def CTRL_KEY(k):
    return ord(k) & 0x1f

E = EditConfig(orig_termios=TtyAttributes(*termios.tcgetattr(STDIN_FILENO)))

class EditorKey(Enum):
    MOVE_LEFT = b'h'
    MOVE_RIGHT = b'l'
    MOVE_UP = b'k'
    MOVE_DOWN = b'j'
    HOME_KEY = b'\x1b[1~'
    DEL_KEY = b'\x1b[3~'
    END_KEY = b'\x1b[4~'
    PAGE_UP = b'\x1b[5~'
    PAGE_DOWN = b'\x1b[6~'
