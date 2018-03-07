# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 19:42:13 2018

@author: Wilson Lab
"""

#==================================================================================================
# MAKE VIDEO OF THE AVERAGE FLUORESCENCE FOR ALL PLANES AND ALL TRIALS
#
# Loads the array of pre-processed imaging data and computes the average fluorescence during each 
# trial for each plane. Then, plots these average images for a single trial in a grid and saves 
# each figure as a frame of a video.
#
# Can handle imaging data with multiple channels.
#
# INPUTS:
#    parentDir = folder with the imaging data files in it
#
#    sids      = a numeric vector specifying the session IDs that you would like to process
#
#==================================================================================================

import os
import numpy as np
import matplotlib.pyplot as plt
from helperFunctions import num_subplots

# def main():
parentDir = os.path.join("B:\Dropbox (HMS)\\2P Data\Imaging Data", '2018_02_25')
sids = [2]
    
for iSession in range(len(sids)):
    
    currSid = sids[iSession]
    fileStr = 'sid_' + str(currSid) + '_Chan_1_sessionFile.npy'
    
    # Load session data file (check for multiple channels)
    sessionData = np.load(os.path.join(parentDir, ('sid_' + str(currSid)), fileStr))
    nTrials = sessionData.shape[4]
    nPlanes = sessionData.shape[2]
    (nPlots, __) = num_subplots(nPlanes)
    
    # Average across volumes
    avgData = sessionData.mean(3)
    
    # Create video writer object
    
    
    # Plot frames and write to video
    for iTrial in range(0, nTrials):  
        
        f = plt.figure(1)
        
        for iPlane in range(nPlanes, 0, -1):  
            plt.subplot(nPlots[0], nPlots[1], iPlane)
            
            # Plot averaged image for each plane
            plt.imshow(avgData[:,:, iPlane - 1, iTrial], cmap='gray')
            
        
        
        
        
        
        
        