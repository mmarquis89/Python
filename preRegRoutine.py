# -*- coding: utf-8 -*-  


#==================================================================================================
# Process raw scanimage data files and save as a single array, as well as saving metadata as a 
# JSON file.
# 
# INPUTS:
#       parentDir   = directory containing the raw data that you want to process.
#
#       sids        = array containing the session IDs you want to process. Pass [] to default to 
#                     detecting and processing all sids present in the parent directory
#
#       expDate     = the date of the experiment in YYYY_MM_DD format
#
# NOTE: the files should be sorted in chronological order due to the timestamp at the beginning 
# of the filename. If filenames do not sort in this pattern, they must be renamed before processing.
#==================================================================================================


import os
import glob
import numpy as np
import tifffile
import time 
from helperFunctions import json_save, save_arr

#--------------------------------------------------------------------------------------------------
# Load data from file and extract metadata
#--------------------------------------------------------------------------------------------------
def read_tif(tifPath):

        # Load file
    with tifffile.TiffFile(tifPath) as tifObj:
    
        # Extract scanimage metadata
        metadata = tifObj.scanimage_metadata['Description']
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

# =================================================================================================  

def main(parentDir, sids, expDate):
        
    # Identify data files for each session
    myFiles = np.array(glob.glob(os.path.join(parentDir, '*sid*tid*.tif')))
    myFiles.sort()
    sessionNums = []
    for iFile in range(0,len(myFiles)):
        currFile = myFiles[iFile]
        sidLoc = currFile.find('sid_')
        sessionNums.append(int(currFile[sidLoc + 4]))
    sessionNums = np.array(sessionNums)
    
    # Identify session numbers to be processed
    if not sids:
        mySessions = list(sorted(set(sessionNums)))
    else:
        mySessions = sids
        
    print('Processing...')
    
    for iSession in range(np.size(mySessions)):
    
        currSid = mySessions[iSession]
        
        # Make session folder for new files if necessary
        sessionDir = os.path.join(parentDir, 'sid_' + str(currSid))
        if not os.path.isdir(sessionDir):
            os.makedirs(sessionDir)
            
        # Separate names of files from the current session
        currFiles = myFiles[sessionNums == currSid]
        
        trialType = []; origFileNames = [];
        tic = time.time()
        for iFile in range(0, len(currFiles)):
            
            # Load a .tif file
            (siData, expInfo, tifArr) = read_tif(currFiles[iFile]) # --> [x, y, plane, volume, channel]
            nChannels = expInfo['nChannels']
            
            # Create output array
            chData = np.zeros(tifArr.shape)
            chData = chData[:,:, 4:, :, :]
            
            for iChan in range(0, nChannels):
                
                # Isolate data for current channel
                currArr = tifArr[:,:,:,:, iChan]                 # --> [x, y, plane, volume]
                
                # Offset so minimum value = 1
                currArr = (currArr - currArr.min()) + 1
                
                # Discard flyback frames
                currArr = currArr[:,:, 4:, :]                   # --> [x, y, plane, volume]
                chData[:,:,:,:, iChan] = currArr                # --> [x, y, plane, volume, channel]
                
            #---- Save to session structure --------
            fName = currFiles[iFile]
            origFileNames.append(fName)
            
            # Get trial type
            if fName.find('StopBall') != -1:
                trialType.append('StopBall')
            elif fName.find('OdorA') != -1:
                trialType.append('OdorA')
            elif fName.find('OdorB') != -1:
                trialType.append('OdorB')
            elif fName.find('NoOdor') != -1 or fName.find('NoStim') != -1:
                trialType.append('NoStim')
            elif fName.find('CarrierStreamStop') != -1:
                trialType.append('CarrierStreamStop')
            elif fName.find('AirStop') != -1:
                trialType.append('AirStop')
            elif fName.find('Laser') != -1:
                trialType.append('Laser')
            else:
                raise NameError('Error: invalid trial type')
                
            # Create session array(s) on first iteration
            if iFile == 0:
                print('Creating session data array(s)...')
                arrSize = list(chData[:,:,:,:, 0].shape)
                arrSize.append(len(currFiles))
                wholeSession_1 = np.uint16(np.zeros(arrSize))  # --> [x, y, plane, volume, trial]
                if nChannels > 1:
                    # Make a second array if there are two channels of imaging data
                    wholeSession_2 = np.uint16(np.zeros(arrSize)) # --> [x, y, plane, volume, trial]
                    
            # Save data to session array(s)
            wholeSession_1[..., iFile] = chData[..., 0]
            if nChannels > 1:
                wholeSession_2[..., iFile] = chData[..., 1]
                
            print('Session ' + str(currSid) + ', Trial #' + str(iFile) + ' of ' + str(len(currFiles)))
         
        print('Trial data processed in ' + str(round(((time.time()-tic) / 60), 1 )) + ' minutes')
        
        tic = time.time()
    
        # Save session data to disk
        if nChannels > 1:
            # Use the red channel to create and save reference images
            refImages = np.zeros((wholeSession_2.shape[0:3]))
            for iPlane in range(0, wholeSession_2.shape[2]):
                refImages[:, :, iPlane] = wholeSession_2[:,:, iPlane, :,:].mean((2,3)) # --> [y, x]
            save_arr(sessionDir, 'sid_' + str(currSid) + '_refImages.npy', refImages)   
                
            # Save each channel as a separate file
            print('Saving channel 1...')
            wholeSession = wholeSession_1
            save_arr(sessionDir, 'sid_' + str(currSid) + '_Chan_1_sessionFile.npy', wholeSession)
            
            print('Saving channel 2...')
            wholeSession = wholeSession_2
            save_arr(sessionDir, 'sid_' + str(currSid) + '_Chan_2_sessionFile.npy', wholeSession)
                
            print('Saving ratio channel...')
            wholeSession = wholeSession_2
            save_arr(sessionDir, 'sid_' + str(currSid) + '_ChanRatio_sessionFile.npy', wholeSession)
            
        else:
            # Use the GCaMP channel to create and save reference images
            refImages = np.zeros((wholeSession_1.shape[0:3]))
            for iPlane in range(0, wholeSession_1.shape[2]):
                refImages[:, :, iPlane] = wholeSession_1[:,:, iPlane, :,:].mean((2,3)) # --> [y, x]
            save_arr(sessionDir, 'sid_' + str(currSid) + '_refImages.npy', refImages)
            
            print('Saving session data...')
            wholeSession = wholeSession_1
            save_arr(sessionDir, 'sid_' + str(currSid) + '_sessionFile.npy', wholeSession)
        
                   
        # Save additional experiment info
        metadata = [trialType, origFileNames, expDate, siData]
        json_save(sessionDir, 'sid_' + str(currSid) + '_metadata.json', metadata)
        
        print('Saving complete in ' + str(round(((time.time()-tic) / 60), 1 )) + ' seconds')

# =================================================================================================    
    
