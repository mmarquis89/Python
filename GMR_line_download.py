# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 14:54:32 2017

@author: Wilson Lab
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Get lists of URLs and line names
url = "http://research.janelia.org/bransonlab/FlyBowl/BehaviorResults/linelist.html"
r = requests.get(url)
nameData = r.text
nameSoup = BeautifulSoup(nameData)
nameBody = nameSoup.body.ul.findAll('a')
lineNames = []
urls = []
for iTag in nameBody:
    urls.append("http://research.janelia.org/bransonlab/FlyBowl/BehaviorResults/" + iTag['href'])
    lineNames.append(iTag.text)

# Scrape data from the page for each line
dfData = pd.DataFrame()
for iLine in range(2001, 2205):

    # Extract table
    url = urls[iLine]
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    table = soup.table.tbody

    # Extract data from each row and add "Line_Name" column
    rows = table.findAll('tr')
    tData = {
        'Behavior_Statistic' : [],
        'Raw_Value' : [],
        'Z_Score' : [],
        'pVal_Greater' : [],
        'pVal_Smaller' : [],
        'Line_Name' : [],
        }
    for iRow in rows:
        cols = iRow.find_all('td')
        tData['Behavior_Statistic'].append(cols[0].get_text())
        tData['Raw_Value'].append(cols[1].get_text())
        tData['Z_Score'].append(cols[2].get_text())
        tData['pVal_Greater'].append(cols[3].get_text())
        tData['pVal_Smaller'].append(cols[4].get_text())
        tData['Line_Name'].append(lineNames[iLine])
        
    # Convert to data frame
    dfData = pd.concat([dfData, pd.DataFrame(tData)], axis=0)
    print(lineNames[iLine])   
  
# Save to .csv file  
dfData.to_csv(dfData['Line_Name'].iloc[1] + '-' + dfData['Line_Name'].iloc[-1] + '.csv')
print("done")
