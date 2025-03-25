# CO2
# The average CO2 is expressed as parts per million (ppm),,,,
# which is the number of molecules of CO2 in every one million,,,,
# molecules of dried air (water vapor removed).  ,,,,
# Missing months are denoted by -99.99.,,,,
# -1 means no data on the number of days,,,,

import matplotlib.pyplot as plt
import pandas as pd
import math

# Extract data from file
co2_data = pd.read_csv("3.2.1_co2_data.csv", header=0)
print(co2_data)

# Clean the data to remove missing months
co2_data['Average'] = co2_data['Average'].replace(-99.99, math.nan)
print(co2_data)
co2_data.dropna(subset=['Average'], inplace=True)
print(co2_data)

# Plot the data
plt.plot(co2_data['decimal_year'], co2_data['Average'], color='gray')
plt.ylabel('Average CO2 in ppm')
plt.xlabel('Years')
plt.title('Change in CO2')

plt.show()
