#!/usr/bin/env python3
import sys

def print_distance_menu():
    print("1. Convert kilometers to miles")
    print("2. Convert miles to kilometers")
    print("3. Quit")
# end def: print_distance_menu

def km_to_miles(km: float) -> float:
    return km * 0.621371
# end def: km_to_miles

def miles_to_km(miles: float) -> float:
    return miles * 1.60934
# end def: miles_to_km

def main():
    print_distance_menu()
    choice = input("Enter your choice: ")

    # add error checking for invalid input
    try:
        if choice == '1':
            km = float(input("Enter distance in kilometers: "))
            miles = km_to_miles(km)
            print("{0} km is equal to {1} miles.".format(km, miles))
        elif choice == '2':
            miles = float(input("Enter distance in miles: "))
            km = miles_to_km(miles)
            print("{0} miles is equal to {1} km.".format(miles, km))
        elif choice == '3':
            print("Goodbye.")
            sys.exit()
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a number.")
# end def: main

if __name__ == '__main__':
    main()
