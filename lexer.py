import re
from typing import List, Tuple, Set, Dict
from collections import defaultdict

# SPIM instruction set obtained from 
# https://www.dejazzer.com/coen4710/projects/1_SPIM_instr.pdf
instructions = '|'.join([
    'syscall', 'add', 'addu', 'addi', 'sub', 'subu', 'div', 'divu', 'rem',
    'remu', 'mul', 'mult', 'multu', 'and', 'andi', 'neg', 'nor', 'not', 'or',
    'ori', 'xor', 'xori', 'sll', 'sllv', 'srl', 'srlv', 'move', 'mfhi', 'mflo',
    'li', 'lui', 'lb', 'sb', 'la', 'lw', 'sw', 'slt', 'slti', 'sltu', 'beq',
    'beqz', 'bge', 'bgez', 'bgezal', 'bgt', 'bgtu', 'bgtz', 'le', 'leu', 'blez',
    'ble', 'bltzal', 'blt', 'bltu', 'bltz', 'bne', 'bnez', 'j', 'jal', 'jr', 
    'jalr'
])
directives = '|'.join([
    'align', 'ascii', 'asciiz', 'byte', 'data', 'double', 'extern', 'float',
    'globl', 'half', 'kdata', 'ktext', 'space', 'text', 'word'
])
token_specs = [
    ('COMMENT', r'#.*'),
    ('DIRECTIVE', fr'\.(?:{directives})\b'),
    ('INSTRUCTION', fr'\b({instructions})\b'),
    ('REGISTER', r'\$[a-zA-Z0-9]+'),
    ('FLOAT', r'-?(\d+\.\d+|\.\d+|\d+\.)'),
    ('INTEGER', r'-?\b\d+\b'),
    ('CHAR', r"'(?:\\[ntr]|\\'|[^\\'])'"),
    ('STRING', r'"[^"]*"'),
    ('LABEL_DEFINITION', r'[a-zA-Z0-9_]+:'),
    ('COMMA', r','),
    ('LBRACKET', r'\('),
    ('RBRACKET', r'\)'),
    ('WHITESPACE', r'\s+'),
    ('UNKNOWN', r'[^\s]+')
]
token_regex = re.compile(
    '|'.join('(?P<%s>%s)' % pair for pair in token_specs)
)

def lex(text: str) -> List[List[Tuple[str, str]]]:
    tokens = initial_lex(text)
    return replace_unknowns_with_labels(tokens, find_labels(tokens))

def initial_lex(text: str) -> List[List[Tuple[str, str]]]:
    tokens = []
    for line in text.splitlines():
        subtokens = []
        for match in token_regex.finditer(line):
            token_type = match.lastgroup
            token_value = match.group()
            subtokens.append((token_type, token_value))
        tokens.append(subtokens)
    return tokens

def find_labels(tokens: List[List[Tuple[str, str]]]) -> List[str]:
    labels = []
    for sub_tokens in tokens:
        for token_type, token_value in sub_tokens:
            if token_type == 'LABEL_DEFINITION':
                label_name = token_value.rstrip(':')
                labels.append(label_name)
    return labels

def replace_unknowns_with_labels(
        tokens: List[List[Tuple[str, str]]], 
        labels: List[str]
    ) -> List[List[Tuple[str, str]]]:
    new_tokens = []
    for sub_tokens in tokens:
        new_subtokens = []
        for token_type, token_value in sub_tokens:
            if token_type == 'UNKNOWN' and token_value in labels:
                token_type = 'LABEL'
            new_subtokens.append((token_type, token_value))
        new_tokens.append(new_subtokens)
    return new_tokens

def count_tokens(tokens: List[List[Tuple[str, str]]]) -> Dict[str, int]:
    token_count = defaultdict(int)
    for subtokens in tokens:
        for token_type, _ in subtokens:
            token_count[token_type] += 1
    return dict(token_count)