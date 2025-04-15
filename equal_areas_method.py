import csv
import matplotlib.pyplot as plt
import numpy as np

"""
    Program calculates characteristic time from bomb calorimetry data using the equal area method and returns T-t vs dT/dt vs t plots
"""

time = []
temp = []
filename = input("What's the name of the data file?")
sample_name = input("What's the name of the sample (for plot titles)?")


# read time and temperature from csv
with open(f'{filename}.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
        time.append(int(row['Time [s]']))
        temp.append(float(row['Temperature [°C]']))

# these thresholds must be adjusted to get the desired boundaries for the rise period
# The plot serves as a helpful tool to do so    
bottom_thresh = 0.04
upper_thresh = 0.0000001

# calculate starting point of the temperature rise period
for i in range(len(time)):
    if (temp[i+1] - temp[i]) >= bottom_thresh:
        ti = time[i]
        Ti = temp[i]
        start_index = i
        break

# calculate tipping point where the temperature rise ends
for f in range(start_index, len(time)):
    if abs(temp[f+1] - temp[f]) <= upper_thresh and abs(temp[f+2] - temp[f+1]) <= upper_thresh:
        tf = time[f]
        Tf = temp[f]
        end_index = f
        break

# calculates the area between the curve and Tf from the right endpoint towards the left up to a certain index
def area_above(index):
    area = 0
    for i in range(index, end_index):
        delta_t = time[i+1]-time[i]
        trapezoid_area = ((Tf-temp[i]) + (Tf-temp[i+1])) * delta_t / 2
        area += trapezoid_area
    return area

# calculates the area between the temperature curve and Ti of rise period from the starting point up to the index
def area_under(index):
    area = 0
    for i in range(start_index, index):
        delta_t = time[i+1] - time[i]
        trapezoid_area = ((temp[i]-Ti)+(temp[i+1]-Ti)) * delta_t / 2
        area += trapezoid_area
    return area

# calculates dT/dt for point on the T-t curve
def slope(index):
    return (temp[index+1]-temp[index]) / (time[index+1] - time[index])

slopes = []

# calculate slopes dT/dt at each datapoint
for index in range(0, min(len(time), len(temp))-1):
    slopes.append(slope(index))


# iterate through time and get the time where the difference between the area above and below is minimized. This approximates tm well.
tm = 0
for i in range(start_index+1, end_index):
    if abs((area_under(i-1) - area_above(i-1))) >= abs((area_under(i) - area_above(i))) and abs((area_under(i) - area_above(i))) <= abs((area_under(i+1) - area_above(i+1))):
        tm = time[i]
        break

# linearly extrapolate pre-period
time_pre = time[:start_index+1]
temp_pre = temp[:start_index+1]

m, b = np.polyfit(time_pre, temp_pre, 1)
def pre_temp(t):
    temperature = m * t + b
    return temperature

# linearly extrapolate post-period
time_post = time[end_index:]
temp_post = temp[end_index:]

a, q = np.polyfit(time_post, temp_post, 1)
def post_temp(t):
    temperature = a * t + q
    return temperature

# calculate DeltaTX = difference between extrapolated temperatures at time=tm
DeltaT_x = post_temp(tm) - pre_temp(tm)

print("DeltaT_x = ", DeltaT_x)

# plot T-t curve and slopes
plt.subplot(1, 2, 1)
plt.plot(time, temp)
plt.xlabel("Time [s]")
plt.ylabel("Temperature [°C]")
# make sure to adjust title accordingly
plt.title(f"Temperature vs Time {sample_name}")

# plot extrapolated pre- and post-periods
plt.plot(time, [pre_temp(t) for t in time], linestyle="--", color="b")
plt.plot(time, [post_temp(t) for t in time], linestyle="--", color="b")

# plot boundaries of rise period and location of tm
plt.axvline(x=ti)
plt.axvline(x=tf)
plt.axvline(x=tm, color='r', linestyle='-')

plt.subplot(1, 2, 2)
plt.plot(time[:-1], slopes)
plt.title(f"dT/dt vs Time for {sample_name}")
plt.xlabel("Time [s]")
plt.ylabel("dT/dt [K/s]")


# also show tm in the slopes plot
plt.axvline(x=tm, color='r', linestyle='-')

plt.show()
