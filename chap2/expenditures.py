#!/usr/bin/env python3
"""
This program graphs weekly expenditures by category. The user is prompted to
enter a series of categories and their weekly expenditures. The program then
displays a bar graph of the expenditures.
"""
import sys
import matplotlib.pyplot as plt

def get_expenditures():
    expenditures = {}
    while True:
        category = input("Enter a category (or 'done' to finish): ")
        if category == 'done':
            break
        else:
            try:
                amount = float(input("Enter the weekly expenditure for {}: ".format(category)))
                expenditures[category] = amount
            except ValueError:
                print("Invalid input.")
    return expenditures
# end def: get_expenditures

def plot_expenditures(expenditures: dict):
    positions = range(1, len(expenditures)+1)
    plt.barh(positions, expenditures.values(), align='center')
    plt.yticks(positions, expenditures.keys())
    plt.ylabel("Category")
    plt.xlabel("Weekly Expenditure")
    plt.title("Weekly Expenditures by Category")
    plt.show()
# end def: plot_expenditures

def main():
    expenditures = get_expenditures()
    plot_expenditures(expenditures)
# end def: main

if __name__ == '__main__':
    main()
# end if
