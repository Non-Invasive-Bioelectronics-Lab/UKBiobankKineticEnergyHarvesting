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
directory = '/data/uk_biobank/data_description/'



diabetes_cols = ('2443-0.0')

# Read in the csv file containing the tabular data on weartime
metadata = pd.read_csv(directory+'ukb23305.csv', sep=',', header=0, low_memory=False)

# GENERATE PLOT OF WEARTIME V. NO. OF PARTICIPANTS
# Empty array to hold data containing number of hours 
lengths = np.zeros([25,2])
# Go through from 0 - 24 hours and see how many participants meet that weartime

filtered_dataset = metadata.dropna()

diabetics = metadata[metadata[diabetes_cols] == 1]
controls = metadata[metadata[diabetes_cols] == 0]
    
diabetics = diabetics['eid']
controls = controls['eid']
    

# Save the eids for the 'good' participants to a csv
diabetics.to_csv('diabetes_records.csv', columns=['eid'], index=False, header=False)
controls.to_csv('non_diabetes_records.csv', columns=['eid'], index=False, header=False)
