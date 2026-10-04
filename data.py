import sys
from dataclasses import dataclass, field, astuple, replace
import termios

sys.dont_write_bytecode = True

# Helper functions
# This one can be replace by importing urses.ascii.iscntrl()
def iscntrl(char):
    char = char.decode("utf-8") # In c we dont have to do this convertion.
    if isinstance(char, str):
        val = int(ord(char)) 
    else:
        val = char
    return (0 <= val <= 31) or (val == 127)

def perror(s: str): # Python automatically halts the program when it encounters and error, so this function and all instances of it are useless unless with a try/excpet.
    _, exc_value, _ = sys.exc_info()
    if exc_value:
        print(f"{s}: {exc_value}", file=sys.stderr)
    else:
        print(s, file=sys.stderr)

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
class EditConfig:
    orig_termios: TtyAttributes
    cx: int = 0
    cy: int = 0
    screenrows: int = 0
    screencols: int = 0

@dataclass
class Winsize:
    ws_rows: int
    ws_col: int
    ws_xpixel: int
    ws_ypixel: int

STDIN_FILENO = sys.stdin.fileno()
STDOUT_FILENO = sys.stdout.fileno()
TIZATL_VERSION = "0.0.1"

def CTRL_KEY(k):
    return ord(k) & 0x1f

#orig_termios = TtyAttributes(*termios.tcgetattr(STDIN_FILENO))
E = EditConfig(orig_termios=TtyAttributes(*termios.tcgetattr(STDIN_FILENO)))
