# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 16:04:09 2018

@author: Wilson Lab
"""

import h5py
import os

#parentDir = 'C:\\Users\Wilson Lab\Documents\MATLAB\\2P_Code'
parentDir = 'B:\Dropbox (HMS)\\2P Data\Imaging Data\\2018_04_26_exp_1\\sid_0'
#filename = 'pyImportTest.mat'
#filename = 'refImages_Reg.mat'
filename = 'Annotations.mat'
myFile = h5py.File(os.path.join(parentDir, filename), 'r')

myKeys = [key for key in myFile.keys()]
myItems = [item for item in myFile.items()]
myVals = [val for val in myFile.values()]



test = []
for iVal in range(0, len(myVals)):
    test[iVal] = myVals[iVal]
     