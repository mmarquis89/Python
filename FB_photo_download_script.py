# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 16:53:52 2020

@author: Wilson Lab
"""
import pyautogui, time, win32clipboard, pytesseract
import pandas as pd

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pyautogui.FAILSAFE = True

# =================================================================================================
# FUNCTION DEFINITIONS
# =================================================================================================

# Find download button icon
def findDlButton():
    
    # Move mouse to menu location and scroll down in case download button is not visible
    menuScrollLoc = (1629, 369)
    pyautogui.moveTo(menuScrollLoc)
    time.sleep(0.1)
    pyautogui.scroll(-1200)
    time.sleep(0.25)    
    dlButtonLoc = pyautogui.locateCenterOnScreen("C:\\Users\\Wilson Lab\\Documents\\Python\\" + 
                                                 "Jupyter\\dl.png", confidence=0.5)
    return dlButtonLoc

# Find menu button icon
def findMenuButton():
    menuButtonLoc = pyautogui.locateCenterOnScreen("C:\\Users\\Wilson Lab\\Documents\\Python\\" + 
                                                   "Jupyter\\menu.png",confidence=0.8)
    return menuButtonLoc

# Find save button icon
def findSaveButton():
    saveButtonGen = pyautogui.locateAllOnScreen("C:\\Users\\Wilson Lab\\Documents\\Python\\" + 
                                                "Jupyter\\save.png",confidence=0.9)
    for loc in saveButtonGen:
        currLoc = pyautogui.center(loc)
        if currLoc[0] > 500:
            return currLoc    
    return None

# Find "next photo" button icon
def findNextButton():
    nextPhotoMouseoverLoc = (1500, 300)
    pyautogui.moveTo(nextPhotoMouseoverLoc) # Hover mouse over "next" button in case it's hidden
    time.sleep(0.25)
    nextButtonLoc = pyautogui.locateCenterOnScreen("C:\\Users\\Wilson Lab\\Documents\\Python\\" + 
                                                   "Jupyter\\next.png",confidence=0.9)
    return nextButtonLoc

# Get contents of currently highlighted text
def copyText():
    pyautogui.hotkey('ctrl', 'c')
    tryCount = 0
    while tryCount <= 5:
        try:
            win32clipboard.OpenClipboard()
            clippedText = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            return clippedText
        except:
            print('Error accessing clipboard...trying again after 1 sec')
            tryCount += 1
            time.sleep(1)
            continue

count = 0
menuScrollLoc = (1629, 369)
uploadDateClickLoc = (1600, 207)
fbidStartLoc = (311, 50)
dateScreenshotRegion = (1600, 198, 150, 25)
trackingList = []
try:
    while True:

        count += 1
        print(count)
        
#        if count > 5:
#            break
        
        uploadDateStr = None
        URLstr = None
        saveFileName = None
        
        # Snip image of region containing photo upload date and extract as string
        im = pyautogui.screenshot(region=dateScreenshotRegion)
        uploadDateStr = pytesseract.image_to_string(im)
        uploadDateStr = uploadDateStr[0:-1] # Drop weird last character
        
        # Copy photo FBID from the URL
        pyautogui.moveTo(fbidStartLoc)
        pyautogui.drag(1000, 0, 0.2)
        URLstr = copyText()
        
        # Click menu button
        pyautogui.click(findMenuButton())
        time.sleep(1)
        
        # Try to find the download button
        findCount = 0
        menuCount = 0
        while findDlButton() is None:
            
            # If it's been a long time, try clicking the menu button again
            if findCount > 10:
                print('Trying the menu button again...')
                pyautogui.click(findMenuButton())
                findCount = 0
                menuCount += 1
                
            # If the menu has already been clicked multiple times, abort the entire process
            if menuCount > 2:
                break
            
            print('Could not find download button...waiting 2 seconds')
            time.sleep(1)
            findCount += 1
            
        # Abort frozen script
        if menuCount > 2: 
            print('Aborting stuck or frozen script')
            break        
        
        # Click download button
        print('Download button found...clicking now')
        pyautogui.click(findDlButton())
        
        # Find save button loc
        saveButtonLoc = findSaveButton()
        while saveButtonLoc is None:
            print('Waiting for save button...')
            time.sleep(0.5) 
            saveButtonLoc = findSaveButton()
        print('Clicking save button...')
        
        # Copy save file name
        saveFileName = copyText()
        
        # Click save button
        pyautogui.click(saveButtonLoc)
        time.sleep(2)
        
        # Click "next photo" button loc
        print('Clicking next photo button...')
        pyautogui.click(findNextButton())
        time.sleep(3)        
            
        # Add info to tracking list
        df_dict = {'uploadDateStr': [uploadDateStr], 'URLstr': [URLstr], 
                   'saveFileName': [saveFileName]}
        newRow = pd.DataFrame(df_dict)
        if count == 1:
            trackingList = newRow
        else:
            trackingList = trackingList.append(newRow)
            
except KeyboardInterrupt:
    print('Quitting script')
    