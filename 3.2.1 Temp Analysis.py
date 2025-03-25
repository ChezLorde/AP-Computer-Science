# a321_temps_analysis.py
# This program uses the pandas module to load a 2-dimensional data sheet into a pandas DataFrame object
# Then it will use the matplotlib module to plot a graph and a bar chart
import matplotlib.pyplot as plt
import pandas as pd

# Load in the data with read_csv()
# (DONE) #1: change the file name to your data file name
temp_data = pd.read_csv("3.2.1_temperature_data.csv", header=0)   # identify the header row

# (DONE) #2: Use matplotlib to make a line graph
plt.plot(temp_data['Year'], temp_data['Anomaly'], color='gray')
plt.ylabel('Temperature Anomalies in Celsius')
plt.xlabel('Years')
plt.title('Change in Temperatures')

# (DONE) #3: Plot LOWESS in a line graph
plt.plot(temp_data['Year'], temp_data['LOWESS'], color='blue')

plt.show()

# (DONE) #4: Use matplotlib to make a bar chart
plt.bar(temp_data['Year'], temp_data['Anomaly'], align='center', color='green')
plt.ylabel('Temperature Anomalies in Celsius')
plt.xlabel('Years')
plt.title('Change in Temperatures')
plt.show()

# TODO #5: Calculate min, max, and avg anomaly and the corresponding min/max years
min_anomaly = temp_data['Anomaly'][0]
max_anomaly = temp_data['Anomaly'][0]
min_year = temp_data['Year'][0]
max_year = temp_data['Year'][0]
sum_anomaly = 0
avg_anomaly = 0

# Find the maximum, minimum and sum values
for i in range(len(temp_data['Anomaly'])):

  sum_anomaly += temp_data['Anomaly'][i]

  if (temp_data['Anomaly'][i] < min_anomaly):
    min_anomaly = temp_data['Anomaly'][i]
    min_year = temp_data['Year'][i]
  elif (temp_data['Anomaly'][i] > max_anomaly):
    max_anomaly = temp_data['Anomaly'][i]
    max_year = temp_data['Year'][i]

# Calculations
avg_anomaly = sum_anomaly / len(temp_data['Anomaly'])

# Prints
print("Minimum Anomaly: " + str(min_anomaly) + ", in year: " + str(min_year))
print("Maximum Anomaly: " + str(max_anomaly) + ", in year: " + str(max_year))
print("Average Anomaly: " + str(avg_anomaly))



  



