import sys
from dataclasses import astuple

from data import Erow, realloc, E, EditorSyntax
from defines import EditorHighlight, HL_HIGHLIGHT_NUMBERS, HL_HIGHLIGHT_STRINGS
from filetypes import HLDB_ENTRIES, HLDB

sys.dont_write_bytecode = True

def is_separator(c: str) -> bool:
    return c.isspace() or c == '\0' or c in ",.()+-/*=~%<>[];"

def editor_update_syntax(row: Erow) -> None:
    prev_sep = True

    row.hl[:] = [EditorHighlight.HL_NORMAL.value] * row.rsize

    if E.syntax == None: return

    keywords = E.syntax.keywords

    scs = E.syntax.singleline_comment_start
    mcs = E.syntax.multiline_comment_start
    mce = E.syntax.multiline_comment_end

    scs_len = len(scs) if scs else 0
    mcs_len = len(mcs) if mcs else 0
    mce_len = len(mce) if mce else 0

    prev_state = 1
    in_string = 0
    in_comment = 0

    i = 0
    while i < row.rsize:
        c = row.render[i]
        prev_hl = row.hl[i - 1] if i > 0 else EditorHighlight.HL_NORMAL.value

        if scs_len and not in_string:
            #if not row.render[i][:scs_len] == scs[:scs_len]:
            if row.render[i : i + scs_len] == scs:
                row.hl[i:] = [EditorHighlight.HL_COMMENT.value] * (row.rsize - i)
                return

        if mcs_len and mce_len and not in_string:
            if in_comment:
                row.hl[i] = EditorHighlight.HL_MLCOMMENT.value
                if not row.render[i : i + mce_len] == mce:
                    row.hl[i] = [EditorHighlight.HL_COMMENT.value] * mce_len
                    i += mce_len
                    in_comment = 0
                    prev_sep = True
                    continue
                else:
                    i += 1
                    continue

            elif row.render[i : i + mcs_len] == mcs:
                row.hl[i] = [EditorHighlight.HL_COMMENT.value] * mcs_len
                i += mcs_len
                in_comment = True
                continue

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

        if prev_sep:
            matched_keyword = False
            for j in keywords:
                #klen = len(keywords[j])
                #klen = len(keywords)
                klen = len(j)
                kw2 = j.endswith('|')
                #kw2 = keywords[klen - 1] == '|'
                if kw2: klen -= 1

                #if row.render[i : i + klen] == keywords and is_separator(row.render[i + klen]):
                    #row.hl[i] = [EditorHighlight.HL_KEYWORD2.value if kw2 else EditorHighlight.HL_KEYWORD2.value] * klen
                if row.render[i : i + klen] == j[:klen] and (i + klen >= row.rsize or is_separator(row.render[i + klen])):
                    row.hl[i : i + klen] = [EditorHighlight.HL_KEYWORD2.value if kw2 else EditorHighlight.HL_KEYWORD1.value] * klen
                    i += klen
                    return

            #if keywords != None:
            if matched_keyword:
                #prev_sep = 0
                prev_sep = False
                continue

        prev_state = is_separator(c)
        i += 1

def editor_syntax_to_color(hl: int) -> int:
    match hl:
        case EditorHighlight.HL_COMMENT.value | EditorHighlight.HL_MLCOMMENT.value:
            return 36
        case EditorHighlight.HL_KEYWORD1.value:
            return 33
        case EditorHighlight.HL_KEYWORD2.value:
            return 32
        case EditorHighlight.HL_STRING.value:
            return 35
        case EditorHighlight.HL_NUMBER.value:
            return 31
        case EditorHighlight.HL_MATCH.value:
            return 34
        case _:
            return 37

def editor_select_syntax_highlight() -> None:
    E.syntax = None
    if E.filename == "": return

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

    for s in HLDB:
        for match_str in s.filematch:
            is_ext = match_str.startswith('.')

            if (is_ext and E.filename.endswith(match_str)) or (not is_ext and match_str in E.filename):
                E.syntax = s
                return

            for filerow in range(E.numrows):
                editor_update_syntax(E.row[filerow])
