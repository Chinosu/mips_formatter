# mips_formatter
A MIPS formatter.

# Usage: 
```bash
python3 main.py <filename>
```

Follows [this](https://jashankj.space/notes/cse-comp1521-better-assembly/) assembly style guide (as of 7 Sep 2023).

# Examples:
## Example 1
**Before:**
```MIPS
.data                   # section for data segment
arr: .word 64, 34, 25, 12, 22, 11, 90 # tree!
size: .word 7 # tree <33333

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
```

**After:**
```MIPS
.data # section for data segment
arr:    .word   64, 34, 25, 12, 22, 11, 90      # tree!
size:   .word   7                               # tree <33333

.text
.globl main
main: # main function start
        la       $t0, arr               # Load base address of array into $t0
        lw       $t1, size              # Load size of array into $t1

# Outer loop
outer_loop:
        li       $t2, 0                 # Initialize inner loop counter to 0
        li       $t3, 1                 # Initialize swapped flag to true (1)

# Inner loop
inner_loop:
        beqz     $t3, outer_end         # If no two elements were swapped by inner loop, then break
        li       $t3, 0                 # Reset swapped flag to false (0)

# Inner loop logic
inner_logic:
        beq      $t2, $t1, inner_end    # If inner loop counter reaches array size, exit inner loop
        lw       $t4, 0($t0)            # Load arr[i] into $t4
        lw       $t5, 4($t0)            # Load arr[i + 1] into $t5
        ble      $t4, $t5, skip_swap    # If arr[i] <= arr[i + 1], skip swap

        # Swap arr[i] and arr[i + 1]
        sw       $t5, 0($t0)
        sw       $t4, 4($t0)
        li       $t3, 1                 # Set swapped flag to true (1)

skip_swap:
        addi     $t0, $t0, 4            # Move to the next element in the array
        addi     $t2, $t2, 1            # Increment inner loop counter
        j        inner_logic

inner_end:
        # Reset array pointer and inner loop counter
        la       $t0, arr
        li       $t2, 0

        # Decrement outer loop counter (size)
        sub      $t1, $t1, 1
        j        outer_loop

outer_end:
        # End of program
        li       $v0, 10                # exit syscall
        syscall

```

## Example 2
**Before:**
```MIPS
.data
prompt1:        .asciiz "Enter the first integer: "
prompt2:        .asciiz "Enter the second integer: "
result_str:     .asciiz "The sum is: "

.text
main:
        # Print the first prompt
        li       $v0, 4                 # System call code for print string
        la       $a0, prompt1           # Load address of the string
        syscall                         # Print the string

        # Read the first integer
        li       $v0, 5                 # System call code for read integer
        syscall                         # Read the integer
        move     $t0, $v0               # Move the read integer to $t0

        # Print the second prompt
        li       $v0, 4                 # System call code for print string
        la       $a0, prompt2           # Load address of the string
        syscall                         # Print the string

        # Read the second integer
        li       $v0, 5                 # System call code for read integer
        syscall                         # Read the integer
        move     $t1, $v0               # Move the read integer to $t1

        # Add the two numbers
        add      $t2, $t0, $t1          # $t2 = $t0 + $t1

        # Print the result
        li       $v0, 4                 # System call code for print string
        la       $a0, result_str        # Load address of the string
        syscall                         # Print the string

        # Print the sum
        move     $a0, $t2               # Move the sum to $a0 for printing
        li       $v0, 1                 # System call code for print integer
        syscall                         # Print the integer

        # Exit the program
        li       $v0, 10                # System call code for exit
        syscall                         # Exit the program
```

**After:**
```MIPS
.data
prompt1:        .asciiz "Enter the first integer: "
prompt2:        .asciiz "Enter the second integer: "
result_str:     .asciiz "The sum is: "

.text
main:
        # Print the first prompt
        li       $v0, 4                 # System call code for print string
        la       $a0, prompt1           # Load address of the string
        syscall                         # Print the string

        # Read the first integer
        li       $v0, 5                 # System call code for read integer
        syscall                         # Read the integer
        move     $t0, $v0               # Move the read integer to $t0

        # Print the second prompt
        li       $v0, 4                 # System call code for print string
        la       $a0, prompt2           # Load address of the string
        syscall                         # Print the string

        # Read the second integer
        li       $v0, 5                 # System call code for read integer
        syscall                         # Read the integer
        move     $t1, $v0               # Move the read integer to $t1

        # Add the two numbers
        add      $t2, $t0, $t1          # $t2 = $t0 + $t1

        # Print the result
        li       $v0, 4                 # System call code for print string
        la       $a0, result_str        # Load address of the string
        syscall                         # Print the string

        # Print the sum
        move     $a0, $t2               # Move the sum to $a0 for printing
        li       $v0, 1                 # System call code for print integer
        syscall                         # Print the integer

        # Exit the program
        li       $v0, 10                # System call code for exit
        syscall                         # Exit the program
```