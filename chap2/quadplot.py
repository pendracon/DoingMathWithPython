#!/usr/bin/env python3
"""
This program plots a series of quadratic values on a graph. Input takes a
starting value for x, a step value for x, and the number of values to
calculate in the series. The program then calculates the corresponding y
values for each x value and plots the points on a graph.
"""
import sys
import matplotlib.pyplot as plt

def main():
    if len(sys.argv) == 4:
        x_start = sys.argv[1]
        x_step = sys.argv[2]
        num_values = sys.argv[3]
    else:
        x_start = input("Enter the starting value for x: ")
        x_step = input("Enter the step value for x: ")
        num_values = input("Enter the number of values to calculate: ")

    try:
        x_start = float(x_start)
        x_step = float(x_step)
        num_values = int(num_values)
    except ValueError:
        print("Invalid input.")
        sys.exit()

    x_values = [x_start + i*x_step for i in range(num_values)]
    y_values = [(x**2 + 2*x + 1) for x in x_values]

    plt.plot(x_values, y_values, 'ro')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Quadratic Values")
    plt.show()
# end def: main

if __name__ == "__main__":
    main()
# end if
