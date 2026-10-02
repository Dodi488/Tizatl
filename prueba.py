from dataclasses import dataclass, field, astuple, replace
import termios
import sys
import array

STDIN_FILENO = sys.stdin.fileno()

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
    screenrows: int = 0
    screencols: int = 0
    #orig_termios: TtyAttributes

@dataclass
class Winsize:
    ws_rows: int
    ws_col: int
    ws_xpixel: int
    ws_ypixel: int

E = EditConfig(orig_termios=TtyAttributes(*termios.tcgetattr(STDIN_FILENO)))

ws = Winsize(0, 0, 0, 0)

p = str(ws)
print(p)
print(type(p))

#encoded = p.encode()
#print(encoded)
#print(type(encoded))

final = array.array('H', list(astuple(ws)))
print(final)
print(type(final))

#if not fcntl.ioctl(STDOUT_FILENO, termios.TIOCGWINSZ, list(astuple(ws))) or ws.ws_col == 0:
#    return -1
#else:
#     col
