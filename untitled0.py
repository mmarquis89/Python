# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 13:52:51 2020

@author: Wilson Lab
"""
import json
import pandas as pd

with open('C:/Users/Wilson Lab/Desktop/test.json') as f:
    testDict = json.load(f)
testDict

df = pd.DataFrame()
for i in testDict.keys():
    currData = testDict[i]
    currData.update({'bodyID':i})
    print(df)
    print(pd.DataFrame(data=currData))
    df = pd.concat([df, pd.DataFrame(data=currData)])

df = df.reindex(sorted(df.columns), axis=1)
df.to_csv('C:/Users/Wilson Lab/Desktop/test.csv')