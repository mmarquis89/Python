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

# Record time script was run
with open('C:/Users/Wilson Lab/Documents/MATLAB/Data/_Server backup logs/BackupScriptLog.txt', 'a') as scriptLog:
    scriptLog.write('\r\n' + time.strftime("%Y-%m-%d %I:%M %p"))

# Open log file with list of new folder paths
pathList = list()
logList = list()
backupQueueFile = 'C:/Users/Wilson Lab/Documents/MATLAB/Data/_Server backup logs/BackupQueueFile.txt'
with open(backupQueueFile, 'r+') as pathFile:
    
    # Write debug check to log
    with open('C:/Users/Wilson Lab/Documents/MATLAB/Data/_Server backup logs/BackupScriptLog.txt', 'a') as scriptLog:
        scriptLog.write('\r\n' + time.strftime("BackupQueueFile Opened"))

    # Load new directory paths from backup queue file
    for line in pathFile:
        pathList.append(line.rstrip('\n'))
        logList.append(line)

    # Copy contents of source directories to server
    for iPath in pathList:
        sh.copytree('C:/Users/Wilson Lab/Documents/MATLAB/Data/' + iPath, 'U:/Data Backup/' + iPath)

    # Write debug check to log
    with open('C:/Users/Wilson Lab/Documents/MATLAB/Data/_Server backup logs/BackupScriptLog.txt', 'a') as scriptLog:
        scriptLog.write('\r\n' + time.strftime("Data copied to server"))
        
# Write copied folder paths to a transfer log file
with open('C:/Users/Wilson Lab/Documents/MATLAB/Data/_Server backup logs/' + time.strftime("%Y-%m-%d") + '.txt', 'a') as logFile:
    sepStr = '\r\n---------------------\r\n'
    logFile.write(sepStr + time.strftime('%Y-%m-%d %I:%M %p') + sepStr + '\r\n')
    for iPath in logList:
        logFile.write(iPath)
    logFile.write('\r\n\r\n')

# Clear copied entries from log file
open(backupQueueFile, 'w').close()
