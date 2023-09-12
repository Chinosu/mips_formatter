import sys
import os

import lexer
import generator

if len(sys.argv) != 2:
    print("Usage: python3 main.py <filename.s> or <filename>.asm")
    sys.exit(1)

file_name = sys.argv[1]

if not os.path.exists(file_name):
    print(f"Error: File {file_name} not found.")
    sys.exit(1)

if not (file_name.endswith('.s') or file_name.endswith('.asm')):
    print("Error: PLease provide a .s or .asm file.")
    sys.exit(1)

tokens = None
with open(file_name, 'r') as file:
    unformatted_code = file.read()
    tokens = lexer.lex(unformatted_code)

if lexer.count_tokens(tokens).get('UNKNOWN', 0) != 0:
    print("Error: UNKNOWN tokens encountered.")
    sys.exit(1)

with open(file_name, 'w') as file:
    formatted_code = generator.generate(tokens)
    for line in formatted_code:
        file.write(line + '\n')