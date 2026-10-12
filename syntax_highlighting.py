import sys
from dataclasses import astuple

from data import Erow, realloc, E, EditorSyntax
from defines import EditorHighlight, HL_HIGHLIGHT_NUMBERS, HL_HIGHLIGHT_STRINGS
from filetypes import HLDB_ENTRIES, HLDB

sys.dont_write_bytecode = True

def is_separator(c: str) -> bool:
    return c.isspace() or c == '\0' or c in ",.()+-/*=~%<>[];"

def editor_update_syntax(row: Erow) -> None:
    row.hl[:] = [EditorHighlight.HL_NORMAL.value] * row.rsize

    if E.syntax == None: return

    prev_state = 1
    in_string = 0

    i = 0
    while i < row.rsize:
        c = row.render[i]
        prev_hl = row.hl[i - 1] if i > 0 else EditorHighlight.HL_NORMAL.value

        if E.syntax.flags & HL_HIGHLIGHT_STRINGS:
            if in_string:
                row.hl[i] = EditorHighlight.HL_STRING.value
                if c == '\\' and (i + 1) < row.rsize:
                    row.hl[i + 1] = EditorHighlight.HL_STRING.value
                    i += 2
                    continue
                if c == in_string: in_string = 0
                i += 1
                prev_sep = 1
                continue

            else:
                if c == '"' or c == '\'':
                    in_string = c
                    row.hl[i] = EditorHighlight.HL_STRING.value
                    i += 1
                    continue

        if E.syntax.flags & HL_HIGHLIGHT_NUMBERS:
            if (c.isdigit() and (prev_state or prev_hl == EditorHighlight.HL_NUMBER.value) or (c == '.' and prev_hl == EditorHighlight.HL_NUMBER.value)):
                row.hl[i] = EditorHighlight.HL_NUMBER.value
                i += 1
                prev_state = 0
                continue

        prev_state = is_separator(c)
        i += 1

def editor_syntax_to_color(hl: int) -> int:
    match hl:
        case EditorHighlight.HL_STRING.value:
            return 35
        case EditorHighlight.HL_NUMBER.value:
            return 31
        case EditorHighlight.HL_MATCH.value:
            return 34
        case _:
            return 37

#def editor_select_syntax_highlight() -> None:
#    E.syntax = None
#    if E.filename == "": return

#    ext = E.filename.find('.')

    #for j in HLDB_ENTRIES:
    #for j in range(len(HLDB)):
#    for j in HLDB:
        #s = EditorSyntax(HLDB.filetype[j])
#        s = HLDB[j]
#        i = 0
        #while s.filematch[i]:
#        for match_str in s.filematch:
#            is_ext = (s.filematch[i][0] == '.')
            #if (is_ext and ext and "." not in s.filematch[i]) or (not is_ext and E.filename in s.filematch[i]):
#            if (is_ext and E.filename.endswith(match_str)) or (not is_ext and match_str in E.filename):
#                E.syntax = s
#                return

#            i += 1

def editor_select_syntax_highlight() -> None:
    E.syntax = None
    if E.filename == "": return

    for s in HLDB:
        for match_str in s.filematch:
            is_ext = match_str.startswith('.')

            if (is_ext and E.filename.endswith(match_str)) or (not is_ext and match_str in E.filename):
                E.syntax = s
                return

                for filerow in range(E.numrows):
                    editor_update_syntax(E.row[filerow])
