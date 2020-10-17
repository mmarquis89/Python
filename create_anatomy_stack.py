# -*- coding: utf-8 -*-

#===================================================================================================
# MAKE AVERAGED ANATOMY STACK FROM INDIVIDUAL 2P VOLUMES

# Will average together all stacks in the directory that meet the requirement specified by 'fileStr'
# and save as .tif files the mean stack as well as a max Z-projection. 
# 
# INPUTS:
#    parentDir        = folder with stack files, e.g. 'B:\Dropbox (HMS)\2P Data\Imaging Data\2017_09_05'
#
#    fileStr          = filter string for dir() selection to get anatomy stack files, e.g. '*stack_*'. 
#                       Be careful to ensure that only the desired files will meet this specification.
#
#    outputFilePrefix = (Default: '') name to prepend to the names of output files.
#===================================================================================================

import os
import glob
import numpy as np
import libtiff
from helperfunctions import read_tif

# =================================================================================================  

def main(parentDir, fileStr, outputFilePrefix=''):
    
    # Identify anatomy stack files
    stacks = np.array(glob.glob(os.path.join(parentDir, fileStr)))
    nStacks = len(stacks)
    
    # Add underscore to prefix if one is provided
    if outputFilePrefix != '':
        outputFilePrefix = outputFilePrefix + '_'
    
    # Get sum of all stacks
    for iVol in range(0, nStacks):
        print('Reading ' + stacks[iVol], '...')
        (siData, expInfo, tifArr) = read_tif(stacks[iVol])
        if iVol == 0:
            firstStack = np.int32(tifArr)       # --> [y, x, plane, volume, channel]
            summedStacks = firstStack           
        else:
            summedStacks += np.int32(tifArr)    # --> [y, x, plane, volume, channel]
    summedStacks.squeeze()
    
    # Check whether there are multiple channels
    if summedStacks.ndim == 3:
        nChannels = 1
    else:
        nChannels = 2
        
    # Calculate mean by dividing by nStacks
    avgStack = summedStacks / nStacks           # --> [y, x, plane, channel]
    
    for iChan in range(0, nChannels):
        
        # Separate data from the current channel
        if nChannels == 1:
            currStack = avgStack
            fileSuffix = ''
        else:
            currStack = avgStack[:,:,:, iChan]
            fileSuffix = '_' + str(iChan + 1)
            
        # Scale array to convert to 8 bit image
        avgStackScaled = currStack - np.min(currStack)                   # --> [y, x, plane]
        avgStackScaled = avgStackScaled / np.max(avgStackScaled)         # --> [y, x, plane]
        avgStackScaled = np.uint8(avgStackScaled * 255).transpose(2,0,1) # --> [plane, y, x]
        
        # Get max Z-projection of averaged stack
        maxZ = np.max(avgStackScaled, 0)                                 # --> [y, x]
        
        # Make sure files with these names don't already exist in the chosen directory
        maxZFileName = os.path.join(parentDir, outputFilePrefix + 'MeanMaxZ' + fileSuffix + '.tif')
        meanStackFileName = os.path.join(parentDir, outputFilePrefix + 'MeanStack' + fileSuffix + '.tif')
        if len(glob.glob(maxZFileName)) > 0 or len(glob.glob(meanStackFileName)) > 0:
               raise NameError('Error: output .tif files already exist in this directory')
    
        # Write averaged stack and Z-projection to .tif files         
        maxZTifObj = libtiff.TIFFimage(maxZ)
        stackTifObj = libtiff.TIFFimage(avgStackScaled)
        maxZTifObj.write_file(maxZFileName)
        stackTifObj.write_file(meanStackFileName)
        
# =================================================================================================  
