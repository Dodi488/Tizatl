import os
import sys

from data import STDOUT_FILENO, E, TIZATL_VERSION
from append_buffer import Abuf, ab_append, ab_free#, ABUF_INIT

sys.dont_write_bytecode = True

def editor_scroll():
    if E.cy < E.rowoff:
        E.rowoff = E.cy

    if E.cy >= E.rowoff + E.screenrows:
        E.rowoff = E.cy - E.screenrows + 1

    if E.cx < E.coloff:
        E.coloff = E.cx

    if E.cx >= E.coloff + E.screencols:
        E.coloff = E.cx - E.screencols + 1

def editor_draw_rows(ab: Abuf) -> None:
    for y in range(E.screenrows):
        filerow = y + E.rowoff
        if (filerow >= E.numrows):
            if (E.numrows == 0 and y == E.screenrows // 3):
                welcome = f"Tizatl editor -- version {TIZATL_VERSION}"
                welcomelen = len(welcome)
                if (welcomelen > E.screencols): welcomelen = E.screencols
                padding = (E.screencols - welcomelen) // 2
                if padding:
                    ab_append(ab, "~", 1)
                    padding -= 1
    
                while padding != 0:
                    ab_append(ab, " ", 1)
                    padding -= 1
                ab_append(ab, welcome, welcomelen)
            else:
                ab_append(ab, "~", 1)

        else:
            length = E.row[filerow].size - E.coloff
            if length < 0: length = 0
            if length > E.screencols: length = E.screencols
            ab_append(ab, E.row[filerow].chars[E.coloff : E.coloff + length], length)
            
        ab_append(ab, "\x1b[K", 3)
        if (y < E.screenrows - 1):
            ab_append(ab, "\r\n", 2)

def editor_refresh_screen() -> None:
    editor_scroll()

    ab = Abuf()

    ab_append(ab, "\x1b[?25l", 6)
    ab_append(ab, "\x1b[H", 3)

    editor_draw_rows(ab)

    buf = f"\x1b[{(E.cy - E.rowoff) + 1};{(E.cx - E.coloff) + 1}H"
    ab_append(ab, buf, len(buf))

    ab_append(ab, "\x1b[?25h", 6)

    os.write(STDOUT_FILENO, ab.b[:ab.length])
    ab_free(ab)
