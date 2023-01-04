# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 14:11:25 2020
generate_cwa_weartime.py
Script to take list of cwa files from the biobank tabulated data and generate 
a text file containing the file names of those that have long enough weartime
Also generates plot of weartime against number of participants
@author: Christopher Beach
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

# Set matplotlib to use constrained_layout as it formats figures better
plt.rcParams['figure.constrained_layout.use'] = True
# Ensure that we don't rasterise text in PDF output
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

# Set seaborn style to get the nice seaborn defaults
sns.set()
# Use seaborn-darkgrid style as it looks better
#plt.style.use('seaborn-darkgrid')

# Directory where the tabular data in the csv file is stored
directory = '//nasr.man.ac.uk/epsrss$/snapped/replicated/casson/data/uk_biobank/install_files/'

# Minimum number of hours in day that sensor must of been worn for (max 24)
# This was 20 in my biobank energy havesting analysis
required_wear = 20
# The names of the columns in the csv file that correspond to the weartime in each day (Monday - Sunday)
weartime_cols = ('90053-0.0', '90054-0.0', '90055-0.0', '90056-0.0', '90057-0.0', '90058-0.0', '90059-0.0')

# Read in the csv file containing the tabular data on weartime
metadata = pd.read_csv(directory+'ukb39617.csv', sep=',', header=0)

# GENERATE PLOT OF WEARTIME V. NO. OF PARTICIPANTS
# Empty array to hold data containing number of hours 
lengths = np.zeros([25,2])
# Go through from 0 - 24 hours and see how many participants meet that weartime
for j in range(25):    
    # Remove all the NaN rows and columns
    filtered_dataset = metadata.dropna()
    # Go through each of the columns containing weartime information for each day
    # and remove those that have a weartime smaller than the desired value for this loop
    for i in weartime_cols:
        filtered_dataset = filtered_dataset[filtered_dataset[i] >= j]
    # Store the number of participants that meet the weartime requirment for this loop
    lengths[j] = [j, len(filtered_dataset)]
    
# Make a plot of weartime v. no. of participants
plt.figure(figsize=(8, 3))
plt.plot(lengths[:,0], lengths[:,1])
plt.xlim([-0.5, 24.5])
plt.xticks(np.linspace(0, 24, num=7))
plt.xlabel('Minimum wear time per day [hours]')
plt.ylabel('Number of participants')
    
# GENERATE CSV FILE WITH DESIRED 'GOOD' RECORDS MEETING THE DESIRED WEARTIME
# Remove all the NaN rows and columns
metadata.dropna(inplace=True)
# Go through each of the columns contating weartime information for each day
# and remove those that have a weartime smaller than the desired value
for i in weartime_cols:
    metadata = metadata[metadata[i] >= required_wear]

# Save the eids for the 'good' participants to a csv
metadata.to_csv('desired_records.csv', columns=['eid'], index=False, header=False)
