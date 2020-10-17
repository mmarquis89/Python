# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 16:53:52 2020

@author: Wilson Lab
"""
import pyautogui, time

# FUNCTION DEFINITIONS

pyautogui.FAILSAFE = True
def findDlButton():
    
    # Move mouse to menu location and scroll down in case download button is not visible
    menuScrollLoc = (1629, 369)
    pyautogui.moveTo(menuScrollLoc)
    time.sleep(0.1)
    pyautogui.scroll(-1200)    
    dlButtonLoc = pyautogui.locateCenterOnScreen("C:\\Users\\Wilson Lab\\Documents\\Python\\Jupyter\\dl.png", confidence=0.5)
    return dlButtonLoc

def findMenuButton():
    menuButtonLoc = pyautogui.locateCenterOnScreen("C:\\Users\\Wilson Lab\\Documents\\Python\\Jupyter\\menu.png",confidence=0.9)
    return menuButtonLoc

def findSaveButton():
    saveButtonGen = pyautogui.locateAllOnScreen("C:\\Users\\Wilson Lab\\Documents\\Python\\Jupyter\\save.png",confidence=0.9)
    for loc in saveButtonGen:
        currLoc = pyautogui.center(loc)
        if currLoc[0] > 500:
            return currLoc    
    return None

def findNextButton():
    nextButtonLoc = pyautogui.locateCenterOnScreen("C:\\Users\\Wilson Lab\\Documents\\Python\\Jupyter\\next.png",confidence=0.9)
    return nextButtonLoc

count = 0
menuScrollLoc = (1629, 369)
try:
    while True:

        count += 1
        print(count)
        
        # Click menu button
        pyautogui.click(findMenuButton())
        time.sleep(1)
                  
        findCount = 0
        while findDlButton() is None:
            # If it's been a long time, try clicking the menu button again
            if findCount > 10:
                print('Trying the menu button again...')
                pyautogui.click(findMenuButton())
                findCount = 0
            print('Could not find download button...waiting 2 seconds')
            time.sleep(1)
            findCount += 1
            
        # Click download button
        print('Download button found...clicking now')
        pyautogui.click(findDlButton())
        time.sleep(1)
        
        # Click save button loc
        saveButtonLoc = findSaveButton()
        while saveButtonLoc is None:
            print('Waiting for save button...')
            time.sleep(0.5) 
            saveButtonLoc = findSaveButton()
        print('Clicking save button...')
        pyautogui.click(saveButtonLoc)
        time.sleep(1)
        
        # Click "next photo" button loc
        print('Clicking next photo button...')
        pyautogui.click(findNextButton())
        time.sleep(1)        
            
except KeyboardInterrupt:
    print('Quitting script')
    