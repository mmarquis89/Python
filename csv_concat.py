# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 16:31:09 2017

@author: Wilson Lab
"""

import csv
from pathlib import Path

filePaths = []
for iPath in Path.cwd().iterdir():
    if iPath.suffix == '.csv':
        filePaths.append(iPath)

lineList = []
for iFile in range(0, len(filePaths)):
    print(str(iFile))
    pathStr = str(filePaths[iFile])
    if pathStr[-10] == '\\':
        lineName = pathStr[-9:-4]
    elif pathStr[-11] == '\\':
        lineName = pathStr[-10:-5]
    elif pathStr[-9] == '\\':
        lineName = pathStr[-8:-4]
        
    reader = csv.reader(open(str(filePaths[iFile]), 'r'))
    if iFile == 1:
        currLine = list(reader)
        colNames = currLine.pop(0)
        colNames.append('lineName')
    else: 
        currLine = list(reader)
        currLine.pop(0)
            
    for iRow in currLine:
        iRow.append(lineName)
        lineList.append(iRow)

print("writing...")
lineList.insert(0, colNames)
with open("GMR_line_data.csv", 'w', newline='') as myFile:
    writer = csv.writer(myFile, quoting=csv.QUOTE_ALL)
    writer.writerows(lineList)


print("done")

