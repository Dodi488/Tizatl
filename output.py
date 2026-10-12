import os
import sys
from time import time

from defines import STDOUT_FILENO, TIZATL_VERSION, EditorHighlight
from syntax_highlighting import editor_syntax_to_color
from data import E
from append_buffer import Abuf, ab_append, ab_free#, ABUF_INIT
from row_operations import editor_row_cx_to_rx

sys.dont_write_bytecode = True

def editor_scroll():
    E.rx = 0

    if E.cy < E.numrows:
        E.rx = editor_row_cx_to_rx(E.row[E.cy], E.cx)

    if E.cy < E.rowoff:
        E.rowoff = E.cy

    if E.cy >= E.rowoff + E.screenrows:
        E.rowoff = E.cy - E.screenrows + 1

    if E.rx < E.coloff:
        E.coloff = E.rx

    if E.rx >= E.coloff + E.screencols:
        E.coloff = E.rx - E.screencols + 1

def editor_draw_rows(ab: Abuf) -> None:
    for y in range(E.screenrows):
        filerow = y + E.rowoff
        if (filerow >= E.numrows):
            if (E.numrows == 0 and y == E.screenrows // 3):
                welcome = f"Tizatl editor -- version {TIZATL_VERSION}"
                welcomelen = len(welcome) if welcomelen > E.screencols else E.screencols
                #welcomelen = len(welcome) if (welcomelen > E.screencols) else welcomelen = E.screencols
                #welcomelen = len(welcome)
                #if welcomelen > E.screencols:
                #    welcomelen = E.screencols
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
            length = E.row[filerow].rsize - E.coloff
            if length < 0: length = 0
            if length > E.screencols: length = len(E.screencols)
            c = E.row[filerow].render[E.coloff:]
            hl = E.row[filerow].hl[E.coloff:]
            current_color = -1
            for j in range(length):
                if hl[j] == EditorHighlight.HL_NORMAL.value:
                    if current_color != -1:
                        ab_append(ab, "\x1b[39m", 5)
                        current_color = -1
                    ab_append(ab, c[j], 1)
                else:
                    color = editor_syntax_to_color(hl[j])
                    if color != current_color:
                        current_color = color
                        buf = "\x1b[{}m".format(color)
                        clen = len(buf)
                        ab_append(ab, buf, clen)
                    ab_append(ab, c[j], 1)

            ab_append(ab, "\x1b[39m", 5)
            
        ab_append(ab, "\x1b[K", 3)
        ab_append(ab, "\r\n", 2)

def editor_draw_status_bar(ab: Abuf) -> None:
    ab_append(ab, "\x1b[7m", 4)

    status = f"{E.filename[:20]} - {E.numrows} lines {"modified" if E.dirty else ""}"
    length = len(status)

    rstatus = f"{E.syntax.filetype if E.syntax else "no ft"} | {E.cy + 1}/{E.numrows}"
    rlength = len(rstatus)

    if length > E.screencols: length = E.screencols
    ab_append(ab, status, length)
    while length < E.screencols:
        if E.screencols - length == rlength:
            ab_append(ab, rstatus, rlength)
            break
        else:
            ab_append(ab, " ", 1)
            length += 1

    ab_append(ab, "\x1b[m", 3)
    ab_append(ab, "\r\n", 2)

def editor_draw_message_bar(ab: Abuf) -> None:
    ab_append(ab, "\x1b[K", 3)
    msglen = len(E.statusmsg)
    if msglen > E.screencols: msglen = E.screencols
    if msglen and time() - E.statusmsg_time < 5:
        ab_append(ab, E.statusmsg, msglen)

def editor_refresh_screen() -> None:
    editor_scroll()

    ab = Abuf()

    ab_append(ab, "\x1b[?25l", 6)
    ab_append(ab, "\x1b[H", 3)

    editor_draw_rows(ab)
    editor_draw_status_bar(ab)
    editor_draw_message_bar(ab)

    buf = f"\x1b[{(E.cy - E.rowoff) + 1};{(E.rx - E.coloff) + 1}H"
    ab_append(ab, buf, len(buf))

    ab_append(ab, "\x1b[?25h", 6)

    os.write(STDOUT_FILENO, ab.b[:ab.length])
    ab_free(ab)

def editor_set_status_message(fmt: str, *args) -> None:
    E.statusmsg = fmt.format(*args)
    E.statusmsg_time = time()
