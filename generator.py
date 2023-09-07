import re
from typing import List, Tuple
from collections import defaultdict

import lexer

tab_len = 8

def generate(tokens: List[List[Tuple[str, str]]]) -> List[str]:
    # For now, the order of horizontal -> vertical is important.
    tokens = add_horizontal_whitespace(tokens) 
    tokens = add_vertical_whitespace(tokens)
    return tokens_to_text(tokens)

def add_horizontal_whitespace(tokens: List[List[Tuple[str, str]]]) -> List[List[Tuple[str, str]]]:
    new_tokens = []
    # Do this first
    for subtokens in tokens:
        new_subtokens = []
        prev_token_type = None
        prev_token_value = None
        prev_prev_token_type = None
        for token_type, token_value in subtokens:
            if token_type == 'INSTRUCTION':
                new_subtokens.append(('WHITESPACE', ' ' * tab_len))
            if prev_token_type == 'INSTRUCTION':
                new_subtokens.append(('WHITESPACE', ' ' * (tab_len - len(prev_token_value))))
            if prev_token_type == 'COMMA' or prev_token_type == 'LABEL_DEFINITION' and not token_type == 'DIRECTIVE' or prev_token_type == 'DIRECTIVE' and not prev_prev_token_type == 'LABEL_DEFINITION' or prev_token_type == 'INSTRUCTION':
                new_subtokens.append(('WHITESPACE', ' '))

            new_subtokens.append((token_type, token_value))
            prev_prev_token_type = prev_token_type
            prev_token_type = token_type
            prev_token_value = token_value
        new_tokens.append(new_subtokens)

    new_tokens = align_right_side_comments(new_tokens)
    new_tokens = align_data_section(new_tokens)
    new_tokens = align_inline_comments(new_tokens)
    return new_tokens

def align_data_section(tokens):
    return align_data_comments(align_data_code(tokens))

def align_data_code(tokens):
    new_tokens = tokens
    longest_len = 0
    for subtokens in new_tokens:
        if len(subtokens) < 2 or not (subtokens[0][0] == 'LABEL_DEFINITION' and subtokens[1][0] == 'DIRECTIVE'):
            continue
        longest_len = max(longest_len, len(subtokens[0][1]))

    multiplier = 0
    while longest_len > tab_len * multiplier:
        multiplier += 1

    for i, subtokens in enumerate(tokens):
        if len(subtokens) < 2 or not (subtokens[0][0] == 'LABEL_DEFINITION' and subtokens[1][0] == 'DIRECTIVE'):
            continue
        new_tokens[i].insert(1, ('WHITESPACE', ' ' * (multiplier * tab_len - len(subtokens[0][1]))))
        new_tokens[i].insert(3, ('WHITESPACE', ' ' * ((multiplier + 1) * tab_len - len(subtokens[0][1]) - len(subtokens[1][1]) - len(subtokens[2][1]))))
    return new_tokens

def align_data_comments(tokens):
    new_tokens = tokens
    longest_len = 0
    for subtokens in new_tokens:
        if not lexer.label_directive_regex.match(tokens_to_line(subtokens)):
            continue
        longest_len = max(longest_len, sum(len(token_value) for _, token_value in subtokens[:-1]))

    multiplier = 0
    while longest_len > tab_len * multiplier:
        multiplier += 1

    for i, subtokens in enumerate(tokens):
        if not lexer.label_directive_regex.match(tokens_to_line(subtokens)):
            continue
        new_tokens[i].insert(len(subtokens) - 1, ('WHITESPACE', ' ' * (tab_len * multiplier - sum(len(token_value) for _, token_value in subtokens[:-1]))))
    return new_tokens

def align_inline_comments(tokens):
    new_tokens = tokens
    for i, subtokens in enumerate(tokens):
        if not (lexer.comment_regex.match(tokens_to_line(subtokens)) and i + 1 < len(tokens) and not lexer.code_label_definition_regex.match(tokens_to_line(tokens[i + 1]))):
            continue
        new_tokens[i].insert(0, ('WHITESPACE', ' ' * tab_len))
    return new_tokens

def align_right_side_comments(tokens):
    new_tokens = tokens
    longest_len = 0
    for subtokens in tokens:
        if not (len(subtokens) > 1 and subtokens[1][0] == 'INSTRUCTION' and subtokens[len(subtokens) - 1][0] == 'COMMENT'):
            continue
        line_len = 1 + sum(len(token_value) for _, token_value in subtokens[:-1])
        longest_len = max(longest_len, line_len)

    multiplier = 0
    while longest_len > tab_len * multiplier:
        multiplier += 1
    
    for i, subtokens in enumerate(tokens):
        if not (len(subtokens) > 1 and subtokens[1][0] == 'INSTRUCTION' and subtokens[len(subtokens) - 1][0] == 'COMMENT'):
            continue
        line_len = sum(len(token_value) for _, token_value in subtokens[:-1])
        new_tokens[i].insert(len(subtokens[:-1]), ('WHITESPACE', ' ' * (multiplier * tab_len - line_len)))
    return new_tokens

def add_vertical_whitespace(
        tokens: List[List[Tuple[str, str]]]
    ) -> List[List[Tuple[str, str]]]:
    new_tokens = []
    for i, subtokens in enumerate(tokens):
        if (i > 0 and 
            len(subtokens) > 1 and
            (subtokens[1][0] == 'COMMENT' or subtokens[0][0] == 'COMMENT') and 
            len(tokens[i - 1]) > 1 and
            tokens[i - 1][1][0] == 'INSTRUCTION'):
            new_tokens.append([('WHITESPACE', '')])
        new_tokens.append(subtokens)
        if len(subtokens) > 0 and is_code_label_definition(subtokens):
            j = i
            while (j > -1 and
                   len(tokens[j]) > 0 and
                   (tokens[j][0][0] == 'COMMENT' or
                    tokens[j][0][0] == 'DIRECTIVE' or
                    is_code_label_definition(tokens[j]))):
                j -= 1
            new_tokens.insert(len(new_tokens) - (i - j), [('WHITESPACE', '')])
    return new_tokens

def is_code_label_definition(tokens: List[List[Tuple[str, str]]]) -> bool:
    return tokens[0][0] == 'LABEL_DEFINITION' and not any(token[0] in [
        'DIRECTIVE', 'INSTRUCTION', 'REGISTER', 'FLOAT', 'INTEGER',
        'CHAR', 'STRING', 'LABEL', 'COMMA', 'LBRACKET', 'RBRACKET'
    ] for token in tokens)

def tokens_to_text(tokens: List[List[Tuple[str, str]]]) -> List[str]:
    lines = []
    for subtokens in tokens:
        line = ''
        for _, token_value in subtokens:
            line += token_value
        lines.append(line)
    return lines

def tokens_to_line(tokens):
    line = ''
    for _, token_value in tokens:
        line += token_value
    return line

    
    