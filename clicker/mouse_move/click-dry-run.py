import pyautogui
from time import sleep
from tqdm import tqdm
import random
# turn off the fail-safe feature. It's just that often when writing scripts that control the mouse, 
# if it gets out of control, you might not be able to use the mouse to close the application.
pyautogui.FAILSAFE = False 

def check_is_digit(input_str):
    """Validate the user input is a number"""
    try:
        if input_str.strip().isdigit():
            return True
        else:
            return False
    except Exception as error:
        print(f"[check_is_digit] Execution failed: {error}")

def mouce_clicker(page_width, page_length):
    """Move the mouse around the screen with a progress bar"""
    try:
        while True:
            max_time = input("Enter seconds to click: ")
            if check_is_digit(max_time):
                for i in tqdm(range(int(max_time)),desc="Progress"):
                    pyautogui.moveTo(random.randint(page_length,page_width), random.randint(page_length,page_width))
                    sleep(1)
                break
            else:
                print("Invalid input, please enter a digit...")
                continue
        return True
    except Exception as error:
        print(f"[mouce_clicker] Execution failed: {error}")

if __name__ == "__main__":
    """This program will calculate the screen size and move the mouse for the requested time"""
    try:
        print(f"Window {pyautogui.size()}")
        page_size = pyautogui.size()
        mouce_clicker(page_size[0], page_size[1])
    except Exception as error:
        print(f"[main] Execution failed: {error}")