import sys

from dataclasses import dataclass
from enum import Enum

sys.dont_write_bytecode = True

STDIN_FILENO = sys.stdin.fileno()
STDOUT_FILENO = sys.stdout.fileno()
TIZATL_VERSION = "0.0.1"
TAB_STOP_SIZE = 4

@dataclass
class EditorKey(Enum):
    BACKSPACE = b'\x7f'
    MOVE_LEFT = b'\x1b[D' #b'h'
    MOVE_RIGHT = b'\x1b[C' #b'l'
    MOVE_UP = b'\x1b[A' #b'k'
    MOVE_DOWN = b'\x1b[B' #b'j'
    HOME_KEY = b'\x1b[1~'
    DEL_KEY = b'\x1b[3~'
    END_KEY = b'\x1b[4~'
    PAGE_UP = b'\x1b[5~'
    PAGE_DOWN = b'\x1b[6~'

class EditorHighlight(Enum):
    HL_NORMAL = 0
    HL_STRING = 1
    HL_NUMBER = 2
    HL_MATCH = 3

HL_HIGHLIGHT_NUMBERS = (1<<0)
HL_HIGHLIGHT_STRINGS = (1<<1)
