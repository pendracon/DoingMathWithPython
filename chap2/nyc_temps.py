#!/usr/bin/env python3
import matplotlib.pyplot as plt

# Plot the annual average temperature in NYC for the years 2000-2012
nyc_temp = [53.9, 56.3, 56.4, 53.4, 54.5, 55.8, 56.8, 55.0, 55.3, 54.0, 56.7, 56.4, 57.3]
years = range(2000, 2013)

plt.plot(years, nyc_temp, marker='o')
plt.xlabel('Year')
plt.ylabel('Temperature')
plt.title('Average annual temperature in NYC')
plt.axis([2000, 2012, 0, 100])
plt.xticks(years)  # Add markers on the x-axis
plt.yticks(range(0, 101, 10))  # Add markers on the y-axis
plt.grid(which='both', axis='both', linestyle=':', linewidth=0.5)  # Optional: light grid lines for reference
#plt.show()
plt.savefig('../tmp/nyc_annual_temps.png')  # Save the plot to a file


# Plot the average monthly temperature in NYC for the years 2000, 2006, and 2012
nyc_temp_2000 = [31.3, 37.3, 47.2, 51.0, 63.5, 71.3, 72.3, 72.7, 66.0, 57.0, 45.3, 31.1]
nyc_temp_2006 = [40.9, 35.7, 43.1, 55.7, 63.1, 71.0, 77.9, 75.8, 66.6, 56.2, 51.9, 43.6]
nyc_temp_2012 = [37.3, 40.9, 50.9, 54.8, 65.1, 71.0, 78.8, 76.7, 68.8, 58.0, 43.9, 41.5]
months = range(1, 13)

plt.plot(months, nyc_temp_2000, months, nyc_temp_2006, months, nyc_temp_2012)
plt.legend([2000, 2006, 2012])
plt.xlabel('Month')
plt.ylabel('Temperature')
plt.title('Average monthly temperature in NYC')
plt.axis([1, 12, 0, 100])
plt.xticks(months)  # Add markers on the x-axis
plt.yticks(range(0, 101, 10))  # Add markers on the y-axis
plt.grid(which='both', axis='both', linestyle=':', linewidth=0.5)  # Optional: light grid lines for reference
#plt.show()
plt.savefig('../tmp/nyc_avg_temps.png')  # Save the plot to a file
