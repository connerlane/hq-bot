import os
import pyautogui

from time import sleep


def save_pic():
    cmd = """osascript -e 'tell app "Image Capture" to activate'"""
    sleep(0.1)
    os.system(cmd)
    pyautogui.click(x=370, y=116)
    pyautogui.click(x=370, y=116, button='right')
    sleep(0.1)
    pyautogui.click(x=393, y=150)
    sleep(0.3)
    cmd = """osascript -e 'tell app "iTerm2" to activate'"""
    os.system(cmd)
