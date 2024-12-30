#!/usr/bin/env python3
"""
This program calculates the Fibonacci sequence, starting from 1, upto n
specified numbers in the sequence and the ratios between them. The ratios are
then plotted on a graph.
"""
import sys
import matplotlib.pyplot as plt

def calculate_fibonacci(n):
    fib_sequence = [1, 1]
    for i in range(2, n):
        fib_sequence.append(fib_sequence[i-1] + fib_sequence[i-2])
    return fib_sequence
# end def: calculate_fibonacci

def calculate_ratios(fib_sequence):
    ratios = [fib_sequence[i] / fib_sequence[i-1] for i in range(1, len(fib_sequence))]
    return ratios
# end def: calculate_ratios

def plot_ratios(ratios):
    plt.plot(ratios, 'b-')
    plt.xlabel("Fibonacci sequence index")
    plt.ylabel("Ratio")
    plt.title("Ratios of Fibonacci numbers")
    plt.show()
# end def: plot_ratios

def main():
    if len(sys.argv) == 2:
        n = sys.argv[1]
    else:
        n = input("Enter a number of Fibonacci numbers to calculate (at least 10): ")

    try:
        n = int(n)
        if n < 10:
            raise ValueError
    except ValueError:
        print("Invalid input.")
        sys.exit()

    fib_sequence = calculate_fibonacci(n)
    print("Sequence:", fib_sequence)

    ratios = calculate_ratios(fib_sequence)
    print("Ratios:", ratios)

    plot_ratios(ratios)
# end def: main

if __name__ == "__main__":
    main()
# end if
