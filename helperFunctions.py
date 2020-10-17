# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 19:26:08 2018

@author: Wilson Lab
"""
import os
import json
import numpy as np


#==================================================================================================                
# FILE I/O FUNCTIONS
#==================================================================================================    

#--------------------------------------------------------------------------------------------------      
# Save object as a JSON text file
def json_save(saveDir, fileName, obj):
    with open(os.path.join(saveDir, fileName), 'xt') as saveFile:
        json.dump(obj, saveFile)    
#--------------------------------------------------------------------------------------------------
    
#--------------------------------------------------------------------------------------------------    
# Save object as an .npy file   
def save_arr(saveDir, fileName, obj):
    with open(os.path.join(saveDir, fileName), 'xb') as saveFile:
        np.save(saveFile, obj)       
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
# Load data from a scanimage .tif file and extract metadata
def read_tif(tifPath):
    import tifffile
    
        # Load file
    with tifffile.TiffFile(tifPath) as tifObj:
    
        # Extract scanimage metadata
        metadata = tifObj.scanimage_metadata['Description']
        if metadata is not None:
            nPlanes = metadata['scanimage.SI.hFastZ.numFramesPerVolume']
            nVolumes = metadata['scanimage.SI.hFastZ.numVolumes']
            nChannels = len(metadata['scanimage.SI.hChannels.channelSave'])
            scanimageData = {'nVolumes':nVolumes, 'nChannels':nChannels}
        
        # Extract image data
        tifArr = tifObj.asarray()
        for iChan in range(0,nChannels):
            currChArr = tifArr[iChan::2, :, :]
            if iChan == 0:
                ySize = currChArr.shape[1]
                xSize = currChArr.shape[2]
                chData = np.empty((ySize, xSize, nPlanes, nVolumes, nChannels))
            chData[:,:,:,:, iChan] = np.transpose(currChArr.reshape(nVolumes, nPlanes, ySize, xSize),
                                                  (2, 3, 1, 0))  # --> [y, x, plane, volume, channel]
    return (metadata, scanimageData, chData)
#--------------------------------------------------------------------------------------------------
   

#==================================================================================================    
# PLOTTING FUNCTIONS
#==================================================================================================    

#--------------------------------------------------------------------------------------------------
# Calculate how many rows and columns are needed for n subplots
def num_subplots(n):
    while is_prime(n) and n > 4:
        n = n + 1
        
    p = prime_factors(n)
    
    if p == 1:
        p = (1, 1)
        return (p, n)
    
    while len(p) > 2:
        if len(p) >= 4:
            p[0] = p[0] * p[-2]
            p[1] = p[1] * p[-1]
            p[-2:] = []
        else:
            p[0] = p[0] * p[1]
            p.pop(1)
        p.sort()
        
    # Reformat if column:row ratio is too large
    while p[1] / p[0] > 2.5:
        N = n + 1
        (p, n) = num_subplots(N)
        
    return (p, n)    
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
# Convert a dimension in pixels to inches for a given DPI
def pix2inch(pixDim, DPI=300):
    inchDim = pixDim / DPI
    return inchDim
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
# Concisely reposition a figure 
# pos = (x, y, w, h)
def set_figpos(f, pos):
    import matplotlib.pyplot as plt
    plt.get_current_fig_manager().window.setGeometry(*pos)
    
#--------------------------------------------------------------------------------------------------

#==================================================================================================    
# MISC FUNCTIONS
#==================================================================================================    

#--------------------------------------------------------------------------------------------------
# Check if a number is prime
def is_prime(n):
    return all(n % i for i in range(2, n))
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
# Calculate all the prime factors of an integer
def prime_factors(n):
    from math import floor
    result = []
    if n == 1:
        return n
    for i in range(2, n + 1): # test all integers between 2 and n
        s = 0;
        while n/i == floor(n/float(i)): # is n/i an integer?
            n = n/float(i)
            s += 1
        if s > 0:
            for k in range(s):
                result.append(i) # i is a pf s times
            if n == 1:
                return result
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def print_loop_status(i, interval = 100):
    if i % interval == 0:
        print(i)
#--------------------------------------------------------------------------------------------------