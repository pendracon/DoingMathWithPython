#!/usr/bin/env python3
"""
This program allows the user to perform various operations with a quadratic equation.

* Written with Copilot+ *
"""
import sys

def get_coefficients():
    a = float(input("Enter the coefficient a: "))
    b = float(input("Enter the coefficient b: "))
    c = float(input("Enter the coefficient c: "))
    return a, b, c
# end def: get_coefficients

def print_operation_menu():
    print("1. Find the roots of a quadratic equation")
    print("2. Express a quadratic equation in standard form")
    print("3. Express a quadratic equation in intercept form")
    print("4. Express a quadratic equation in vertex form")
    print("5. Quit")
# end def: print_operation_menu

def print_roots(a: float, b: float, c: float):
    discriminant = (b**2 - 4*a*c)**0.5

    if type(discriminant) is complex or discriminant > 0:
        root1 = (-b + discriminant) / (2*a)
        root2 = (-b - discriminant) / (2*a)
        print("The roots are {0} and {1}.".format(root1, root2))
    elif discriminant == 0:
        root = -b / (2*a)
        print("The root is {0}.".format(root))
    else:
        real_part = -b / (2*a)
        imaginary_part = (-discriminant)**0.5 / (2*a)
        print("The roots are {0} + {1}j and {0} - {1}j.".format(real_part, imaginary_part))
# end def: print_roots

def print_standard_form(a: float, b: float, c: float):
    print("The standard form of the equation is {0}x^2 + {1}x + {2}.".format(a, b, c))
# end def: print_standard_form

def print_intercept_form(a: float, b: float, c: float):
    x_intercept1 = (-b + (b**2 - 4*a*c)**0.5) / (2*a)
    x_intercept2 = (-b - (b**2 - 4*a*c)**0.5) / (2*a)
    y_intercept = c

    print("The intercept form of the equation is y = {0}(x - {1})(x - {2}).".format(a, x_intercept1, x_intercept2))
    print("The y-intercept is {0}.".format(y_intercept))
# end def: print_intercept_form

def print_vertex_form(a: float, b: float, c: float):
    x_vertex = -b / (2*a)
    y_vertex = a*x_vertex**2 + b*x_vertex + c

    print("The vertex form of the equation is y = {0}(x - {1})^2 + {2}.".format(a, x_vertex, y_vertex))
    print("The vertex is ({0}, {1}).".format(x_vertex, y_vertex))
# end def: print_vertex_form

def main():
    a, b, c = 0, 0, 0

    do_loop = True
    do_prompt = True

    try:
        if len(sys.argv) == 4:
            a = float(sys.argv[1])
            b = float(sys.argv[2])
            c = float(sys.argv[3])
            do_loop = False
            do_prompt = False
        
        while True:
            if do_prompt:
                a, b, c = get_coefficients()

            print_operation_menu()
            choice = input("Enter your choice: ")

            if choice == '1':
                print_roots(a, b, c)
            elif choice == '2':
                print_standard_form(a, b, c)
            elif choice == '3':
                print_intercept_form(a, b, c)
            elif choice == '4':
                print_vertex_form(a, b, c)
            elif choice == '5':
                print("Goodbye.")
                sys.exit()
            else:
                print("Invalid choice.")

            if do_loop:
                do_again = input("Do another operation? (y/n): ")
                do_loop = do_again.lower() == 'y'
            
            if not do_loop:
                break
    except ValueError:
        print("Invalid input. Please enter numbers only.")
# end def: main

if __name__ == '__main__':
    main()
