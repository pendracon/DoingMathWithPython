#!/usr/bin/env python3
"""
A simple fractions calculator.
This program will take two fractions and an operation to perform as input and
print the result of the operation.

* Written with Copilot+ *
"""
import sys
from fractions import Fraction

def get_fraction() -> Fraction:
    fraction = input("Enter a fraction (e.g. 1/2): ")
    return Fraction(fraction)
# end def: get_fraction

def add(f1: Fraction, f2: Fraction) -> Fraction:
    return f1 + f2
# end def: add

def subtract(f1: Fraction, f2: Fraction) -> Fraction:
    return f1 - f2
# end def: subtract

def multiply(f1: Fraction, f2: Fraction) -> Fraction:
    return f1 * f2
# end def: multiply

def divide(f1: Fraction, f2: Fraction) -> Fraction:
    return f1 / f2
# end def: divide

def execute_operation(f1: Fraction, f2: Fraction, operation: str, prompt_again: bool = True) -> bool:
    if operation == '+':
        result = add(f1, f2)
    elif operation == '-':
        result = subtract(f1, f2)
    elif operation == '*':
        result = multiply(f1, f2)
    elif operation == '/':
        result = divide(f1, f2)
    else:
        print("Invalid operation.")
        sys.exit(1)

    print(f1, operation, f2, "=", result)

    do_again = ''
    if prompt_again:
        do_again = input("Do another calculation? (y/n): ")

    return do_again.lower() == 'y'
# end def: execute_operation
    
def main():
    # add support for cli arguments to pass fractions and operation
    # in infix, polish, and reverse polish notation
    if len(sys.argv) > 1:
        if len(sys.argv) != 4:
            print("Usage: python fractions_calc.py [[f1 op f2] [f1 f2 op] [op f1 f2]]")
            sys.exit(1)

        a1 = sys.argv[1]
        a2 = sys.argv[2]
        a3 = sys.argv[3]
        try:
            if a1 in ['+', '-', '*', '/']:
                operation = a1
                f1 = Fraction(a2)
                f2 = Fraction(a3)
            elif a2 in ['+', '-', '*', '/']:
                operation = a2
                f1 = Fraction(a1)
                f2 = Fraction(a3)
            elif a3 in ['+', '-', '*', '/']:
                operation = a3
                f1 = Fraction(a1)
                f2 = Fraction(a2)
            else:
                print("Invalid arguments.")
                sys.exit(1)
        except ValueError:
            print("Invalid fraction.")
            sys.exit(1)
        execute_operation(f1, f2, operation, False)
    else:
        while True:
            f1 = get_fraction()
            f2 = get_fraction()
            operation = input("Enter an operation (+, -, *, /): ")
            do_again = execute_operation(f1, f2, operation)
            if not do_again:
                break
            else:
                print()
# end def: main

if __name__ == '__main__':
    main()
