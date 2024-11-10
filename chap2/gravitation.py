#!/usr/bin/env python3
import matplotlib.pyplot as plt

# Gravitational constant: 6.674 * 10^-11 N(m/kg)^2
# Force = G * (m1 * m2) / r^2
# G = Gravitational constant
# m1 = Mass of first object
# m2 = Mass of second object
# r = Distance between the centers of the masses
G = 6.674*(10**-11)

def draw_graph(x, y):
    plt.plot(x, y, marker='o')
    plt.xlabel('Distance in meters')
    plt.ylabel('Gravitational force in newtons')
    plt.title('Gravitational force and distance')
    # plt.xticks(x)  # Add markers on the x-axis
    # plt.yticks(y)  # Add markers on the y-axis
    plt.grid(which='both', axis='both', linestyle=':', linewidth=0.5)  # Optional: light grid lines for reference
    plt.show()
# end def: draw_graph

def generate_F_r(m1: float, m2: float, r: list):
    F = []
    for dist in r:
        force = G*(m1*m2)/(dist**2)
        F.append(force)

    draw_graph(r, F)
# end def: generate_F_r

def main():
    m1 = 0.5
    m2 = 1.5
    r = range(100, 1001, 50)
    generate_F_r(m1, m2, r)
# end def: main

if __name__ == '__main__':
    main()
