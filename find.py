import sys

from data import E
from row_operations import editor_row_rx_to_cx

sys.dont_write_bytecode = True

def editor_find_callback(query: str, key: bytes) -> None:
    if key == b'\r' or key == '\x1b':
        return

    for i in range(E.numrows):
        row = E.row[i]
        match = row.render.find(query)
        if match != -1:
            E.cy = i
            E.cx = editor_row_rx_to_cx(row, match)
            E.rowoff = E.cy
            return

def editor_find() -> None:
    from input import editor_prompt
    query = editor_prompt("Search: {} (ESC to cancel)", editor_find_callback)
