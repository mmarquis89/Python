# -*- coding: utf-8 -*-

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
#    parentDir    = folder with the imaging data files in it
#
#    sids         = a numeric vector specifying the session IDs that you would like to process
# 
#    nChannels    = (default: 1) the number of imaging channels used in the experiment
#
#    maxIntensity = (default: 900) integer value to use as max intensity for plotting 
#    
#==================================================================================================

import os
import numpy as np
import matplotlib.pyplot as plt
from helperfunctions import num_subplots, set_figpos

def main(parentDir, sids, nChannels=1, maxintensity=900):
    
    for iSession in range(len(sids)):
    
        currSid = sids[iSession]
        
        if nChannels == 1:
            fileStr = 'sid_' + str(currSid) + '_sessionFile.npy'
        else:
            fileStr = 'sid_' + str(currSid) + '_Chan_1_sessionFile.npy'
        
        # Load session data file (check for multiple channels)
        sessionData = np.load(os.path.join(parentDir, ('sid_' + str(currSid)), fileStr)) # --> [y, x, plane, volume, channel]
        nTrials = sessionData.shape[4]
        nPlanes = sessionData.shape[2]
        (nPlots, __) = num_subplots(nPlanes)
        
        # Average across volumes
        avgData = sessionData.mean(3) # --> [y, x, plane, volume, channel]                                                   
        
        # Plot frames and write to image files
        for iTrial in range(0, nTrials):  
            print('Trial #' + str(iTrial))
            
            f = plt.figure(1, dpi=300) # w x h
            set_figpos(f, (-1900, 50, 1800, 920))
            
            for iPlane in range(nPlanes, 0, -1):  
                plt.subplot(nPlots[0], nPlots[1], iPlane)
                
                # Plot averaged image for each plane
                plt.imshow(avgData[:,:, iPlane - 1, iTrial], cmap='gray', vmax=maxintensity)
                if iPlane == nPlanes:
                    plt.title('Ventral', {'fontsize':4})
                elif iPlane == 1:
                    plt.title('Dorsal', {'fontsize':4})
                plt.suptitle('Trial #' + str(iTrial + 1), fontsize=6)
                plt.tick_params(bottom='off', left='off', labelleft='off', labelbottom='off')
                
            # Adjust subplot spacing
            plt.subplots_adjust(left=0.02, 
                                right=0.98, 
                                top=0.975, 
                                bottom=0, 
                                wspace=0.03, 
                                hspace=0)
            
            # Create save directory if necessary
            saveDir = os.path.join(parentDir, 'sid_' + str(currSid) + '_Avg_fluorescence_frames')
            if not os.path.isdir(saveDir):
                os.makedirs(saveDir)
                
            # Save frame as .png file
            fileName = 'Trial_' + str(iTrial) + '_avg_fluorescence.png'
            plt.savefig(os.path.join(saveDir, fileName), dpi='figure')
            plt.close(f)
        
        # Create video from individual trial frames
        fileStr = 'Trial_%d_avg_fluorescence.png'
        vidFileName = os.path.join(parentDir, 'sid_' + str(currSid) + '_avg_fluorescence.mov')
        dirCommand = 'cd /d ' + saveDir + ''
        vidCommand = 'ffmpeg -framerate 1 -i ' + fileStr + ' -vcodec prores -r 1 -y "' + vidFileName + '"'
        os.system(dirCommand + ' & ' + vidCommand)

        
        