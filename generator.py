import re
from typing import List, Tuple
from collections import defaultdict

def generate(tokens: List[List[Tuple[str, str]]]) -> List[str]:
    # For now, the order of horizontal -> vertical is important.
    tokens = add_horizontal_whitespace(tokens) 
    tokens = add_vertical_whitespace(tokens)
    return tokens_to_text(tokens)

def add_horizontal_whitespace(
        tokens: List[List[Tuple[str, str]]]
    ) -> List[List[Tuple[str, str]]]:
    tab_length = 8
    new_tokens = []
    for i, subtokens in enumerate(tokens):
        new_subtokens = []
        prev_token_type = None
        prev_token_value = None
        prev_prev_token_type = None
        for token_type, token_value in subtokens:
            if token_type == 'INSTRUCTION':
                new_subtokens.append(('WHITESPACE', ' ' * tab_length))
            if (prev_token_type == 'COMMA' or 
                prev_token_type == 'LABEL_DEFINITION' and not token_type == 'DIRECTIVE' or 
                prev_token_type == 'DIRECTIVE' and not prev_prev_token_type == 'LABEL_DEFINITION' or
                not prev_token_type == None and token_type == 'COMMENT'):
                new_subtokens.append(('WHITESPACE', ' '))
            if prev_token_type == 'INSTRUCTION':
                new_subtokens.append(('WHITESPACE', ' ' * (tab_length - len(prev_token_value))))
            if token_type == 'DIRECTIVE' and prev_token_type == 'LABEL_DEFINITION':
                new_subtokens.append(('WHITESPACE', ' ' * (tab_length - len(prev_token_value))))
            if prev_prev_token_type == 'LABEL_DEFINITION' and prev_token_type == 'DIRECTIVE':
                new_subtokens.append(('WHITESPACE', ' ' * (tab_length - len(prev_token_value))))
            new_subtokens.append((token_type, token_value))
            prev_prev_token_type = prev_token_type
            prev_token_type = token_type
            prev_token_value = token_value
        new_tokens.append(new_subtokens)
        if (i < len(tokens) - 1 and
            subtokens[0][0] == 'COMMENT' and
            len(subtokens) == 1 and
            not tokens[i + 1][0][0] == 'LABEL_DEFINITION'):
            new_tokens[i].insert(0, ('WHITESPACE', ' ' * tab_length))
    longest_line = 0;
    for subtokens in new_tokens:
        line_length = 0
        for token_type, token_value in subtokens:
            line_length += len(token_value) if not token_type == 'COMMENT' else 0
        longest_line = line_length if line_length > longest_line else longest_line
    smallest_multiplier = 0
    while longest_line > tab_length * smallest_multiplier:
        smallest_multiplier += 1
    for i, subtokens in enumerate(tokens):
        if (subtokens[len(subtokens) - 1][0] == 'COMMENT' and
            len(new_tokens[i]) > 1 and
            new_tokens[i][1][0] == 'INSTRUCTION'):
            length = 0
            for _, token_value in new_tokens[i][:-1]:
                length += len(token_value)
            new_tokens[i].insert(len(new_tokens[i]) - 1, ('WHITESPACE', ' ' * (smallest_multiplier * tab_length - length)))
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