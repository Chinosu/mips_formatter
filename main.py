import tokenizer

test_code = '''
.data               # section for data segment
prompt: .asciiz "Enter an integer: "
result: .asciiz "The factorial is: "

.text
.globl main

main:              # main function start
    # Prompt the user for input
    li $v0, 4
    la $a0, prompt
    syscall

    # Read the integer from the user
    li $v0, 5
    syscall
    move $t0, $v0  # $t0 stores the integer n

    # Initialize $t1 to store the factorial, starting from 1
    li $t1, 1

    # Check if n is zero or negative
    blez $t0, output

    # Loop to calculate factorial
    loop:
        mul $t1, $t1, $t0  # $t1 = $t1 * $t0
        sub $t0, $t0, 1    # $t0 = $t0 - 1
        bgtz $t0, loop     # if $t0 > 0, repeat loop

    # Output the result
    output:
        li $v0, 4
        la $a0, result
        syscall

        move $a0, $t1
        li $v0, 1
        syscall

    # Exit the program
    li $v0, 10
    syscall
'''

print(f'Original:\n{test_code}')

print('')

tokens = tokenizer.tokenize(test_code)
for i, subtokens in enumerate(tokens):
    print(f'Tokens for line {i + 1}: {subtokens}')

print('')

token_count = tokenizer.count_tokens(tokens)
for token_type in token_count.keys():
    print(f'There are {token_count[token_type]} counts of token type {token_type}')