# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 11:45:01 2020

@author: Wilson Lab
"""

import os
import time
import piexif

# Get lists of file names
dir_1 = r'C:\Users\Wilson Lab\Documents\Python\output'
dir_2 = r'B:\New folder'
dir_1_files = os.listdir(dir_1)
dir_2_files = os.listdir(dir_2)
dir_1_files = [i for i in dir_1_files if i[-4:] == '.jpg']
dir_2_files = [i for i in dir_2_files if i[-4:] == '.jpg']

missingFiles = []
wrongDateFiles = []
validDateFiles = []
for idx, iFile in enumerate(dir_1_files):
    
    if idx % 100 == 0:
        print(idx)
    
    # Extract FB photo ID from file name
    fbID = iFile[10:-4]
    
    # Extract date taken from file name
    dateTakenTime = time.strptime(iFile[0:8], '%Y%m%d')
    
    # Search list of files in second directory for one containing the fbID
    matchFileName = None
    for jFile in dir_2_files:
        if fbID in jFile:
            matchFileName = jFile
    
    # Note any files for which no match was found
    if matchFileName is None:
        missingFiles.append(iFile)
    else:
        # Update "date taken" field in second file if dateTakenTime is valid
        if iFile[0:8] != '20201016':
            exif_dict = piexif.load(os.path.join(dir_2, matchFileName))
            exif_dict['Exif'] = {piexif.ExifIFD.DateTimeOriginal: 
                                time.strftime('%Y:%m:%d %H:%M:%S', dateTakenTime)}
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, os.path.join(dir_2, matchFileName))
            validDateFiles.append(iFile)
            
            # Rename updated file
            os.rename(os.path.join(dir_2, matchFileName), os.path.join(dir_2, iFile))
            
        else:
            wrongDateFiles.append(iFile)
        
    
    
    
    
    
    
    
    
    
    
    
    