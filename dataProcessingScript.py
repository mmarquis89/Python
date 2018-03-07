# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 12:33:46 2018

@author: Wilson Lab
"""
import os
import importlib

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
# NoRMCorre registration
#==================================================================================================