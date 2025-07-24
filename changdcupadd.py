import pyperclip
import pyautogui
import time
plist=None


with open(f"addinglist.txt","r",encoding="UTF-8") as f:
    plist = f.readlines()

for i in plist:
    url=i
    print(url)
    pyperclip.copy(url)
    pyautogui.moveTo(480, 630)
    pyautogui.leftClick()
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.moveTo(889, 676)
    pyautogui.leftClick()
    pyautogui.moveTo(480, 630)
    pyautogui.leftClick()
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('backspace')
    

