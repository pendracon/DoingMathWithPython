#!/usr/bin/env python3
"""
A simple program to convert units between:
- distances between kilometers and miles.
- weights between kilograms and pounds.
- temperatures between Celsius and Fahrenheit.

* Written with Copilot+ *
"""
import sys

def print_main_menu():
    print("1. Distance")
    print("2. Weight")
    print("3. Temperature")
    print("4. Quit")
# end def: print_main_menu

def print_distance_menu():
    print("1. Convert kilometers to miles")
    print("2. Convert miles to kilometers")
    print("3. Cancel")
# end def: print_distance_menu

def print_weight_menu():
    print("1. Convert kilograms to pounds")
    print("2. Convert pounds to kilograms")
    print("3. Cancel")
# end def: print_weight_menu

def print_temperature_menu():
    print("1. Convert Celsius to Fahrenheit")
    print("2. Convert Fahrenheit to Celsius")
    print("3. Cancel")
# end def: print_temperature_menu

def distance():
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
            pass
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a number.")
# end def: distance

def weight():
    print_weight_menu()
    choice = input("Enter your choice: ")

    # add error checking for invalid input
    try:
        if choice == '1':
            kg = float(input("Enter weight in kilograms: "))
            pounds = kg_to_pounds(kg)
            print("{0} kg is equal to {1} pounds.".format(kg, pounds))
        elif choice == '2':
            pounds = float(input("Enter weight in pounds: "))
            kg = pounds_to_kg(pounds)
            print("{0} pounds is equal to {1} kg.".format(pounds, kg))
        elif choice == '3':
            pass
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a number.")
# end def: weight

def temperature():
    print_temperature_menu()
    choice = input("Enter your choice: ")

    # add error checking for invalid input
    try:
        if choice == '1':
            celsius = float(input("Enter temperature in Celsius: "))
            fahrenheit = celsius_to_fahrenheit(celsius)
            print("{0} Celsius is equal to {1} Fahrenheit.".format(celsius, fahrenheit))
        elif choice == '2':
            fahrenheit = float(input("Enter temperature in Fahrenheit: "))
            celsius = fahrenheit_to_celsius(fahrenheit)
            print("{0} Fahrenheit is equal to {1} Celsius.".format(fahrenheit, celsius))
        elif choice == '3':
            pass
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a number.")
# end def: temperature

def km_to_miles(km: float) -> float:
    return km * 0.621371
# end def: km_to_miles

def miles_to_km(miles: float) -> float:
    return miles * 1.60934
# end def: miles_to_km

def kg_to_pounds(kg: float) -> float:
    return kg * 2.20462
# end def: kg_to_pounds

def pounds_to_kg(pounds: float) -> float:
    return pounds * 0.453592
# end def: pounds_to_kg

def celsius_to_fahrenheit(celsius: float) -> float:
    return celsius * 9/5 + 32
# end def: celsius_to_fahrenheit

def fahrenheit_to_celsius(fahrenheit: float) -> float:
    return (fahrenheit - 32) * 5/9
# end def: fahrenheit_to_celsius

def main():
    # add error checking for invalid input
    while True:
        print_main_menu()
        choice = input("Enter your choice: ")

        try:
            if choice == '1':
                distance()
            elif choice == '2':
                weight()
            elif choice == '3':
                temperature()
            elif choice == '4':
                print("Goodbye.")
                sys.exit()
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input. Please enter a number.")

        print()
# end def: main

if __name__ == '__main__':
    main()
