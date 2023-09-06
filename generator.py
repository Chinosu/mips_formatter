import re
from typing import List, Tuple, Set, Dict
from collections import defaultdict



# TODO: add support for whitespace



def generate(tokens):
    lines = []
    for subtokens in tokens:
        lines.append(generate_line(subtokens))
    lines = [line for line in lines if line.strip()]
    return lines

def generate_line(tokens):
    line = ''
    for i, (token_type, token_value) in enumerate(tokens):
        if token_type == 'WHITESPACE' or token_type == 'UNKNOWN':
            continue
        prev_token_type = tokens[i - 1][0] if i > 0 else None
        prev_prev_token_type = tokens[i - 2][0] if i > 1 else None
        if prev_prev_token_type == 'INSTRUCTION':
            line += ' ' * (16 - len(line))
        elif token_type == 'INSTRUCTION':
            line += ' ' * 8
        elif line and not token_type == 'COMMA' and not token_type == 'LBRACKET' and not token_type == 'RBRACKET'and not prev_token_type == 'LBRACKET':
            line += ' '
        line += token_value
    return line 
