import sys

from data import E
from defines import EditorKey, EditorHighlight
from row_operations import editor_row_rx_to_cx

sys.dont_write_bytecode = True

last_match = -1
direction = 1

saved_hl_line = 0
saved_hl = ""

def editor_find_callback(query: str, key: bytes) -> None:
    global last_match, direction, saved_hl_line, saved_hl

    if saved_hl:
        E.row[saved_hl_line].hl = saved_hl
        saved_hl = []

    if key == b'\r' or key == '\x1b':
        last_match = -1
        direction = 1
        return
    elif key == EditorKey.MOVE_RIGHT.value or key == EditorKey.MOVE_DOWN.value:
        direction = 1
    elif key == EditorKey.MOVE_LEFT.value or key == EditorKey.MOVE_UP.value:
        direction = -1
    else:
        last_match = -1
        direction = 1

    if last_match == -1: direction = 1
    current = last_match
    for i in range(E.numrows):
        current += direction
        if current == -1: current = E.numrows - 1
        elif current == E.numrows: current = 0

        row = E.row[current]
        match = row.render.find(query)
        if match != -1:
            last_match = current
            E.cy = current
            E.cx = editor_row_rx_to_cx(row, match)
            E.rowoff = E.cy

            saved_hl_line = current
            saved_hl = list(row.hl)
            row.hl[match : match + len(query)] = [EditorHighlight.HL_MATCH.value] * len(query)
            return

def editor_find() -> None:
    saved_cx = E.cx
    saved_cy = E.cy
    saved_coloff = E.coloff
    saved_rowoff = E.rowoff

    from input import editor_prompt
    query = editor_prompt("Search: {} (Use ESC/Aroow/Enter)", editor_find_callback)

    if query:
        return
    else:
        E.cx = saved_cx
        E.cy = saved_cy
        E.coloff = saved_coloff
        E.rowoff = saved_rowoff
