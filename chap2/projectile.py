#!/usr/bin/env python3
"""
This program calculates the trajectory of a projectile based on the initial
velocity and launch angle. Multiple trajectories can be plotted together by
providing them as a comma-separated list of initial velocities, e.g.:
    
    $ python projectile.py 10,20 45
"""
import math
import matplotlib.pyplot as plt
import sys

# Projectile velocity: v = u + at
# Projectile displacement: s = ut + 0.5at^2
# u = Initial velocity
# v = Final velocity
# a = Acceleration
# t = Time
# s = Displacement

G = 9.8  # Acceleration due to gravity in m/s^2

def plot_graph(x, y):
    plt.plot(x, y, linewidth=2)
    plt.xlabel('Distance in meters')
    plt.ylabel('Height in meters')
    plt.title('Projectile motion of a ball')
    plt.grid(which='both', axis='both', linestyle=':', linewidth=0.5)  # Optional: light grid lines for reference
# end def: draw_graph

def calculate_trajectory(u, theta, t):
    theta = math.radians(theta)  # Convert angle to radians

    # Calculate the x and y coordinates
    x = u * math.cos(theta) * t
    y = u * math.sin(theta) * t - 0.5 * G * t**2

    return x, y
# end def: calculate_trajectory

def calculate_flight_times(u, theta):
    flight_times = []
    if not isinstance(u, list):
        u = [u]

    theta = math.radians(theta)  # Convert angle to radians

    # Calculate the times of flight
    for vel in u:
        t = round(2 * vel * math.sin(theta) / G, 5)
        flight_times.append(t)

    return flight_times
# end def: calculate_flight_times

def frange(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step
# end def: frange

def main():
    do_loop = True
    do_prompt = True

    if len(sys.argv) == 3:
        initial_velocity = sys.argv[1]
        launch_angle = sys.argv[2]
        do_loop = False
        do_prompt = False

    while True:
        try:
            if do_prompt:
                initial_velocity = input("Enter the initial velocity (m/s): ")
                launch_angle = input("Enter the launch angle (degrees): ")

            launch_angle = float(launch_angle)
            initial_velocities = []
            for ivel in initial_velocity.split(','):
                initial_velocities.append(float(ivel.strip()))

            t_flights = calculate_flight_times(initial_velocities, launch_angle)
            #print("Time of flight (velocities={0}, angle={1}): {2}s".format(initial_velocities, launch_angle, t_flights))

            for i, t_flight in enumerate(t_flights):
                intervals = frange(0, t_flight, 0.001)
                x_coords = []
                y_coords = []

                for t in intervals:
                    x, y = calculate_trajectory(initial_velocities[i], launch_angle, t)
                    x_coords.append(x)
                    y_coords.append(y)

                plot_graph(x_coords, y_coords)
                print("Trajectory (velocity={0}m/s, angle={1}d): flight time = {2}s, max height = {3:.2f}m, max distance = {4:.2f}m".
                      format(initial_velocities[i], launch_angle, t_flight, max(y_coords), max(x_coords)))

            if len(initial_velocities) > 1:
                plt.legend(initial_velocities, title='Initial Velocities', loc='upper right')
            plt.show()
        except ValueError:
            print("You entered an invalid input.")
        
        if do_loop:
            if input("Do you want to continue (y/n)? ").lower() != 'y':
                do_loop = False

        if not do_loop:
            if do_prompt:
                print("Goodbye!")
            break
        else:
            print()
# end def: main

if __name__ == '__main__':
    main()
