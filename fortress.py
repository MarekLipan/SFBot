"""
Obtained resourcess
"""

import pyautogui
import random
import time
import webbrowser

# =============================================================================
# PARAMS
# =============================================================================

no_soldiers = 30  # Stop attack after all soldiers are depleted

# =============================================================================
# FUNCTION DEFINITION
# =============================================================================

def single_attack():
    """
    Attack on a random player with a single soldier.
    """
    time.sleep(random.uniform(0.2, 0.3))
    pyautogui.press("enter")
    time.sleep(random.uniform(0.2, 0.3))
    pyautogui.press("right")
    time.sleep(random.uniform(0.2, 0.3))
    # attacking phase
    pyautogui.press("enter")
    time.sleep(random.uniform(0.6, 0.8))
    pyautogui.press("enter")
    time.sleep(random.uniform(0.2, 0.3))
    pyautogui.press("enter")
    time.sleep(random.uniform(0.2, 0.3))
    return


def log_in():
    """
    Logs into the game
    """

    webbrowser.open('http://www.seznam.cz')
    pyautogui.moveTo((600, 85), duration=0.6)
    time.sleep(random.uniform(0.1, 0.2))
    pyautogui.click(button="left")
    time.sleep(random.uniform(0.1, 0.2))
    pyautogui.press("s")
    time.sleep(random.uniform(0.1, 0.2))
    pyautogui.press("f")
    time.sleep(random.uniform(0.3, 0.6))
    pyautogui.press("enter")

    return


# =============================================================================
# START
# =============================================================================
# log into the game and load it
time.sleep(3)
log_in()
time.sleep(10)
# open the fortress
pyautogui.moveTo((450, 875), duration=0.6)
time.sleep(random.uniform(0.1, 0.2))
pyautogui.click(button="left")
# start attacking
for i in range(no_soldiers):
    single_attack()

# buy full stock of soldiers
pyautogui.moveTo((1700, 220), duration=0.6)
time.sleep(random.uniform(0.1, 0.2))
pyautogui.click(button="left")
time.sleep(random.uniform(0.1, 0.2))
pyautogui.moveTo((1600, 970), duration=0.6)
time.sleep(random.uniform(0.1, 0.2))
pyautogui.click(button="left")

print("THE END")
# =============================================================================
# END OF FILE
# =============================================================================

