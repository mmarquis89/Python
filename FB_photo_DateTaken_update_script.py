# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 11:39:33 2020

@author: Wilson Lab
"""

import os
import pickle
import re
import piexif
import time


parentDir = r'B:\New folder'

# Find and load all .pkl files, then concatenate their contents
dirFiles = os.listdir(parentDir)
dirFiles = [i for i in dirFiles if i[-4:] == '.pkl']
for idx, iFile in enumerate(dirFiles):
    print(idx)
    with open(os.path.join(parentDir, iFile), 'rb') as f:
        data = pickle.load(f)
    if idx == 0:
        df = data
    else:
        df = df.append(data)

# ---------- Parse upload dates ----------
dateList = [i.strip() for i in list(df.uploadDateStr)]

# Extract individual date components
yearList = [re.search(r'\d{4}', i).group() for i in dateList]
monthList = [re.search(r'\A.*? ', i).group().strip() for i in dateList]
dayList = [re.search(r' \d{1,2},', i).group().strip()[:-1]
            if re.search(r' \d{1,2},', i) is not None 
            else  '1' for i in dateList]

# Fix "Apri" entries in monthList
monthList = [re.sub('Apri\Z', 'April', i) for i in monthList]

# Combine into dates
fullDates = [i+j+k for i, j, k in zip(yearList, monthList, dayList)]
fullDateStrings = [time.strftime('%Y:%m:%d %H:%M:%S', time.strptime(i, '%Y%B%d')) 
                    for i in fullDates]






