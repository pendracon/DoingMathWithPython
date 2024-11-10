#!/usr/bin/env python3
"""
This program finds all the multiples of a given number upto the nth multiple.

* Written with Copilot+ *
"""
import sys

def multi_table(num, count: int = 10) -> list:
    '''
    Find and return all the products of the given number from 1 upto 'count'
    multiples.
    '''
    products = []

    for i in range(1, count+1):
        products.append(num * i)
    
    return products
# end def: multi_table

def main():
    base_num = 0

    do_loop = True
    do_prompt_num = True
    do_prompt_count = True

    if len(sys.argv) > 1:
        base_num = sys.argv[1]
        do_loop = False
        do_prompt_num = False

    if len(sys.argv) > 2:
        count = sys.argv[2]
        do_prompt_count = False

    while True:
        if do_prompt_num:
            base_num = input("Enter a number to multiply: ")
        if do_prompt_count:
            count = input("Enter number of multiples to find: ")

        try:
            if not float(base_num):
                print("Must enter a number to multiply.")
            elif len(count) > 0 and not float(count).is_integer():
                print("Must enter an integral for the number of multiples.")
            else:
                float_table = False
                if base_num.find('.') > -1:
                    base_num = float(base_num)
                    float_table = True
                else:
                    base_num = int(base_num)

                if len(count) > 0:
                    multiples = multi_table(base_num, int(count))
                else:
                    multiples = multi_table(base_num)

                for i in range(len(multiples)):
                    if float_table:
                        print("{0:.2f} x {1} = {2:.2f}".format(base_num, i+1, multiples[i]))
                    else:
                        print("{0} x {1} = {2}".format(base_num, i+1, multiples[i]))
        except ValueError:
            print("Invalid input. Please enter whole numbers.")

        if do_loop:
            do_again = input("Do another calculation? (y/n): ")
            do_loop = do_again.lower() == 'y'

        if not do_loop:
            break
        else:
            print()
# end def: main

if __name__ == '__main__':
    main()
