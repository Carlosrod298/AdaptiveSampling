
# Importing Statistics module
import statistics

# Creating a sample of data
sample = [2.74, 1.23, 2.63, 2.22, 3, 1.98]

# Prints variance of the sample set



VarianceT = [2679,2631,2642,2581,2608,2634,2638,2606,2609,2622,2578,2581,2573,2604,2606,2587,2591,2606,2581,2577,2576,
             2526,2535,2497,2497,2539,2536,2517,2495,2496]
VarianceH = [6973,7370,7408,6965,7066,7416,7057,7212,6979,7375,7057,6879,6934,7406,7132,6965,7285,7164,6867,6992,6981,
             7622,7298,7189,7114,7682,7375,7308,7137,7122]

# Function will automatically calculate
# it's mean and set it as xbar
print("Variance of Temperature sample set is % s" %(statistics.variance(VarianceT)))
print("Variance of Humidity sample set is % s" %(statistics.variance(VarianceH)))