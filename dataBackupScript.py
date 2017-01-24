# -*- coding: utf-8 -*-

"""
===============================================================================
Automatically copies data in a list of folders specified by a log file created
by Matlab (BackupQueueFile.txt) and transfers it to a backup folder on the
server. Will then clear the names of the copied folders from the original log
file and save a new file with today's date containing the names of the folders
that were copied.
===============================================================================
"""

import shutil as sh
import time

# Open log file with list of new folder paths
pathList = list()
logList = list()
backupQueueFile = 'C:/Users/Wilson Lab/Documents/MATLAB/Data/_Server backup logs/BackupQueueFile.txt'
with open(backupQueueFile, 'r+') as pathFile:

    # Load new directory paths from backup queue file
    for line in pathFile:
        pathList.append(line.rstrip('\n'))
        logList.append(line)

    # Copy contents of source directories to server
    for iPath in pathList:
        sh.copytree('C:/Users/Wilson Lab/Documents/MATLAB/Data/' + iPath, 'U:/Data Backup/' + iPath)

# Write copied folder paths to a transfer log file
with open('C:/Users/Wilson Lab/Documents/MATLAB/Data/_Server backup logs/' + time.strftime("%Y-%m-%d") + '.txt', 'w') as logFile:
    for iPath in logList:
        logFile.write(iPath)

# Clear copied entries from log file
open(backupQueueFile, 'w').close()
