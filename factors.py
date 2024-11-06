#!/usr/bin/env python3
import sys

def factor(num: int) -> list:
    '''
    Find and return all the factors of the given number.
    '''
    factors = []

    if num != 0:
        signer = -1 if num < 0 else 1

        for i in range(1, abs(num)+1):
            if abs(num) % i == 0:
                factors.append(i * signer)
                factors.append(-i * signer)
    
    return sorted(factors)
# end def: factor

def main():
    num_to_factor = 0

    if len(sys.argv) == 2:
        num_to_factor = sys.argv[1]
    else:
        num_to_factor = input("Enter a number to factor: ")

    try:
        if not float(num_to_factor).is_integer():
            print("Must enter a whole number to factor.")
        else:
            print(factor(int(num_to_factor)))
    except ValueError:
        print("Invalid input. Please enter a whole number.")
# end def: main

if __name__ == '__main__':
    main()
