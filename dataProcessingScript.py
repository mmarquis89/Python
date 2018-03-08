# -*- coding: utf-8 -*-

import os
os.chdir('Documents\Python')
import importlib

#==================================================================================================
# Create anatomy stacks
#==================================================================================================


#==================================================================================================
# Pre-registration processing
#==================================================================================================
import preRegRoutine; importlib.reload(preRegRoutine)

expDates = ['2018_02_25', 
            ]
         
sids = [2, 
        ]            
            
for iExp in range(0, len(expDates)):
    parentDir = os.path.join("B:\Dropbox (HMS)\\2P Data\Imaging Data", expDates[iExp])
    preRegRoutine.main(parentDir, sids, expDates[iExp])

del expDates, sids, parentDir


#==================================================================================================
# Make trial-averaged fluorescence vids
#==================================================================================================
import create_avg_fluorescence_vid; importlib.reload(create_avg_fluorescence_vid)

expDates = ['2018_02_25', 
            ]
         
sids = [2, 
        ]  

for iExp in range(0, len(expDates)):
    parentDir = os.path.join("B:\Dropbox (HMS)\\2P Data\Imaging Data", expDates[iExp])
    create_avg_fluorescence_vid.main(parentDir, sids, nChannels=2)

del expDates, sids, parentDir


#==================================================================================================
# NoRMCorre registration
#==================================================================================================