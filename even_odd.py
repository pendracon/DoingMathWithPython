#!/usr/bin/env python3
"""
An even or odd number vending machine.
This program will take a number as input and:
1. Print whether the number is 'even' or 'odd'; and
2. Print the next 10 even or odd numbers.
"""
import sys

def get_even_odd(num: int) -> str:
    return 'even' if num % 2 == 0 else 'odd'
# end def: get_even_odd

def get_next_ten(num: int) -> list:
    next_ten = range(num + 2, num + 22, 2)
    return list(next_ten)
# end def: get_next_ten

def main():
    num_to_vend = 0

    if len(sys.argv) == 2:
        num_to_vend = sys.argv[1]
    else:
        num_to_vend = input("Enter a number to vend even or odd: ")

    try:
        if not float(num_to_vend).is_integer():
            print("Must enter a whole number to vend.")
        else:
            print("The number is:", get_even_odd(int(num_to_vend)))
            print("The next 10 numbers are:", get_next_ten(int(num_to_vend)))
    except ValueError:
        print("Invalid input. Please enter a whole number.")
# end def: main

if __name__ == '__main__':
    main()
