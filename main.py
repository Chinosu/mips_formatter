import lexer
import generator

test_code = '''
.data                   # section for data segment
arr: .word 64, 34, 25, 12, 22, 11, 90
size: .word 7

.text
.globl main

main:  # main function start
    la $t0, arr         # Load base address of array into $t0
    lw $t1, size        # Load size of array into $t1

    # Outer loop
    outer_loop:
        li $t2, 0       # Initialize inner loop counter to 0
        li $t3, 1       # Initialize swapped flag to true (1)
        # Inner loop
        inner_loop:
            beqz $t3, outer_end   # If no two elements were swapped by inner loop, then break
            li $t3, 0             # Reset swapped flag to false (0)
            # Inner loop logic
            inner_logic:
                beq $t2, $t1, inner_end  # If inner loop counter reaches array size, exit inner loop
                lw $t4, 0($t0)           # Load arr[i] into $t4
                lw $t5, 4($t0)           # Load arr[i + 1] into $t5
                ble $t4, $t5, skip_swap  # If arr[i] <= arr[i + 1], skip swap
                # Swap arr[i] and arr[i + 1]
                sw $t5, 0($t0)
                sw $t4, 4($t0)
                li $t3, 1               # Set swapped flag to true (1)
                skip_swap:
                addi $t0, $t0, 4        # Move to the next element in the array
                addi $t2, $t2, 1        # Increment inner loop counter
                j inner_logic

            inner_end:
            # Reset array pointer and inner loop counter
            la $t0, arr
            li $t2, 0
            # Decrement outer loop counter (size)
            sub $t1, $t1, 1
            j outer_loop

        outer_end:
        # End of program
        li $v0, 10          # exit syscall
        syscall

'''

tokens = lexer.lex(test_code)
for i, subtokens in enumerate(tokens):
    print(f'Tokens for line {i + 1}: {subtokens}')

print('')

token_count = lexer.count_tokens(tokens)
for token_type in token_count.keys():
    print(f'There are {token_count[token_type]} counts of token type {token_type}')

# formatted_code = generator.generate(tokens)
# for line in formatted_code:
#     print(line)