"""
Collecting data
"""

import numpy as np
import pyautogui
from PIL import ImageGrab
import time
import random
import os
import cv2 as cv
import time


main_path = "/Users/marek/Desktop/Projects/SFBot/"

# =============================================================================
# PARAMS
# =============================================================================
min_uncollected_items_to_attack = 3
max_no_attacks = 100
max_scans_per_search = 50
max_no_searches = 10
min_search_rank = 5000
max_search_rank = 40000
x, y = 1547, 197
item_width = 100
item_height = 145
vertical_gap = 172
horizontal_gap_small = 174
horizontal_gap_big = 236

# =============================================================================
# FUNCTION DEFINITION
# =============================================================================
items = [
    "helmet",
    "chest",
    "gloves",
    "boots",
    "weapon",
    "necklace",
    "belt",
    "ring",
    "talisman"
]

dic_items = {}

for i in items:
    save_path = os.path.join(main_path, "data", "collected_items", i)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    save_path = os.path.join(main_path, "data", "not_collected_items", i)
    if not os.path.exists(save_path):
        os.makedirs(save_path)


# load not collected data
dic_items["not_collected_helmet"] = os.listdir(os.path.join(main_path, "data", "not_collected_items", "helmet"))
dic_items["not_collected_chest"] = os.listdir(os.path.join(main_path, "data", "not_collected_items", "chest"))
dic_items["not_collected_gloves"] = os.listdir(os.path.join(main_path, "data", "not_collected_items", "gloves"))
dic_items["not_collected_boots"] = os.listdir(os.path.join(main_path, "data", "not_collected_items", "boots"))
dic_items["not_collected_weapon"] = os.listdir(os.path.join(main_path, "data", "not_collected_items", "weapon"))
dic_items["not_collected_necklace"] = os.listdir(os.path.join(main_path, "data", "not_collected_items", "necklace"))
dic_items["not_collected_belt"] = os.listdir(os.path.join(main_path, "data", "not_collected_items", "belt"))
dic_items["not_collected_ring"] = os.listdir(os.path.join(main_path, "data", "not_collected_items", "ring"))
dic_items["not_collected_talisman"] = os.listdir(os.path.join(main_path, "data", "not_collected_items", "talisman"))

# load collected data
dic_items["collected_helmet"] = os.listdir(os.path.join(main_path, "data", "collected_items", "helmet"))
dic_items["collected_chest"] = os.listdir(os.path.join(main_path, "data", "collected_items", "chest"))
dic_items["collected_gloves"] = os.listdir(os.path.join(main_path, "data", "collected_items", "gloves"))
dic_items["collected_boots"] = os.listdir(os.path.join(main_path, "data", "collected_items", "boots"))
dic_items["collected_weapon"] = os.listdir(os.path.join(main_path, "data", "collected_items", "weapon"))
dic_items["collected_necklace"] = os.listdir(os.path.join(main_path, "data", "collected_items", "necklace"))
dic_items["collected_belt"] = os.listdir(os.path.join(main_path, "data", "collected_items", "belt"))
dic_items["collected_ring"] = os.listdir(os.path.join(main_path, "data", "collected_items", "ring"))
dic_items["collected_talisman"] = os.listdir(os.path.join(main_path, "data", "collected_items", "talisman"))


def item_image_grab(vg, hgb,hgs):
    """
    Grabs part of screen depicting an image of an item from character screen in hall of fame.

    :param vg: Number of vertical gaps to take in respect to original coordinates
    :param hgb:  Number of big horizontal gaps to take in respect to original coordinates
    :param hgs:  Number of small horizontal gaps to take in respect to original coordinates
    :return: PIL.Image
    """
    img = ImageGrab.grab(
        bbox=(
            x + hgb * horizontal_gap_big + hgs * horizontal_gap_small,
            y + vg * vertical_gap,
            x + item_width + hgb * horizontal_gap_big + hgs * horizontal_gap_small,
            y + item_height + vg * vertical_gap
        ))

    return img


def get_item_name(img):
    """
    Translate PIL image into the array and then get the mean pixel from each of RGB channels.
    Returns string of the image name, which at the same time is the image representation code.

    :param img: Input PIL.Image
    :return: string
    """
    # image representation stored in the name
    mean_colours = np.array(img).mean(axis=(0, 1))
    item_name = str(mean_colours[0]) + "_" + str(mean_colours[1]) + "_" + str(mean_colours[2]) + ".png"

    return item_name


def check_collected_item(item, item_slot, uncollected_items, collected_list, not_collected_list):
    """
    Chek if the item is collected, else saves the image of not collected item and updates the respective list

    :param item: Image of the target item
    :param item_slot: Item slot name of the target item
    :param not_collected_list:  List of not collected items of the target item
    :return: string
    """

    item_name = get_item_name(item)

    if item_name in collected_list:
        pass
    else:
        uncollected_items += 1
        if item_name not in not_collected_list:
            item.save(os.path.join(main_path, "data", "not_collected_items", item_slot, item_name))
            not_collected_list.append(item_name)

    return uncollected_items, not_collected_list


def attack_collect_item(item, item_slot, collected_list, not_collected_list):
    """
    Collect all items that the targeted opponents has

    :param item: Image of the target item
    :param item_slot: Item slot name of the target item
    :param not_collected_list:  List of not collected items of the target item
    :return: string
    """

    item_name = get_item_name(item)

    if item_name in collected_list:
        pass
    elif item_name in not_collected_list:
        os.rename(
            os.path.join(main_path, "data", "not_collected_items", item_slot, item_name),
            os.path.join(main_path, "data", "collected_items", item_slot, item_name)
        )
        collected_list.append(item_name)
        not_collected_list.remove(item_name)
    else:
        item.save(os.path.join(main_path, "data", "collected_items", item_slot, item_name))
        collected_list.append(item_name)

    return collected_list, not_collected_list


def attack_and_store(dic_items):
    """
    Attack the current shown opponent and add the items to the collected ones
    """

    time.sleep(random.uniform(1.1, 1.4))
    pyautogui.press("num9")
    time.sleep(random.uniform(1.1, 1.4))
    pyautogui.press("enter")
    time.sleep(random.uniform(1.1, 1.4))
    pyautogui.press("enter")
    time.sleep(random.uniform(1.1, 1.4))
    pyautogui.press("enter")
    time.sleep(random.uniform(1.1, 1.4))

    # scan now once again
    helmet = item_image_grab(0, 0, 0)
    dic_items["collected_helmet"], dic_items["not_collected_helmet"] = attack_collect_item(helmet, "helmet", dic_items["collected_helmet"], dic_items["not_collected_helmet"])

    chest = item_image_grab(1, 0, 0)
    dic_items["collected_chest"], dic_items["not_collected_chest"] = attack_collect_item(chest, "chest", dic_items["collected_chest"], dic_items["not_collected_chest"])

    gloves = item_image_grab(2, 0, 0)
    dic_items["collected_gloves"], dic_items["not_collected_gloves"] = attack_collect_item(gloves, "gloves", dic_items["collected_gloves"], dic_items["not_collected_gloves"])

    boots = item_image_grab(3, 0, 0)
    dic_items["collected_boots"], dic_items["not_collected_boots"] = attack_collect_item(boots, "boots", dic_items["collected_boots"], dic_items["not_collected_boots"])

    weapon_1 = item_image_grab(3, 1, 0)
    dic_items["collected_weapon"], dic_items["not_collected_weapon"] = attack_collect_item(weapon_1, "weapon", dic_items["collected_weapon"], dic_items["not_collected_weapon"])

    weapon_2 = item_image_grab(3, 1, 1)
    dic_items["collected_weapon"], dic_items["not_collected_weapon"] = attack_collect_item(weapon_2, "weapon", dic_items["collected_weapon"], dic_items["not_collected_weapon"])

    necklace = item_image_grab(0, 2, 1)
    dic_items["collected_necklace"], dic_items["not_collected_necklace"] = attack_collect_item(necklace, "necklace", dic_items["collected_necklace"], dic_items["not_collected_necklace"])

    belt = item_image_grab(1, 2, 1)
    dic_items["collected_belt"], dic_items["not_collected_belt"] = attack_collect_item(belt, "belt", dic_items["collected_belt"], dic_items["not_collected_belt"])

    ring = item_image_grab(2, 2, 1)
    dic_items["collected_ring"], dic_items["not_collected_ring"] = attack_collect_item(ring, "ring", dic_items["collected_ring"], dic_items["not_collected_ring"])

    talisman = item_image_grab(3, 2, 1)
    dic_items["collected_talisman"], dic_items["not_collected_talisman"] = attack_collect_item(talisman, "talisman", dic_items["collected_talisman"], dic_items["not_collected_talisman"])

    return dic_items


def search(dic_items):
    """
    Searches until finds a good target
    """

    i = 0

    while i < max_no_searches:
        i += 1

        # click to search cell
        pyautogui.moveTo((1000, 1300), duration=0.3)
        pyautogui.click(button="left")
        time.sleep(random.uniform(0.05, 0.15))

        # generate and write the position for search
        generated_position = str(random.randint(min_search_rank, max_search_rank))
        for s in generated_position:
            pyautogui.press(s)
            time.sleep(random.uniform(0.05, 0.15))

        pyautogui.press("enter")
        time.sleep(1)

        # start scanning
        j = 0
        while j < max_scans_per_search:
            j += 1

            # scroll down
            pyautogui.press("down")

            # make sure everything is refreshed
            time.sleep(random.uniform(0.08, 0.12))

            uncollected_items = 0

            # scanning
            helmet = item_image_grab(0, 0, 0)
            uncollected_items, dic_items["not_collected_helmet"] = check_collected_item(helmet, "helmet", uncollected_items, dic_items["collected_helmet"], dic_items["not_collected_helmet"])

            chest = item_image_grab(1, 0, 0)
            uncollected_items, dic_items["not_collected_chest"] = check_collected_item(chest, "chest", uncollected_items, dic_items["collected_chest"], dic_items["not_collected_chest"])

            gloves = item_image_grab(2, 0, 0)
            uncollected_items, dic_items["not_collected_gloves"] = check_collected_item(gloves, "gloves", uncollected_items, dic_items["collected_gloves"], dic_items["not_collected_gloves"])

            boots = item_image_grab(3, 0, 0)
            uncollected_items, dic_items["not_collected_boots"] = check_collected_item(boots, "boots", uncollected_items, dic_items["collected_boots"], dic_items["not_collected_boots"])

            weapon_1 = item_image_grab(3, 1, 0)
            uncollected_items, dic_items["not_collected_weapon"] = check_collected_item(weapon_1, "weapon", uncollected_items, dic_items["collected_weapon"], dic_items["not_collected_weapon"])

            weapon_2 = item_image_grab(3, 1, 1)
            uncollected_items, dic_items["not_collected_weapon"] = check_collected_item(weapon_2, "weapon", uncollected_items, dic_items["collected_weapon"], dic_items["not_collected_weapon"])

            necklace = item_image_grab(0, 2, 1)
            uncollected_items, dic_items["not_collected_necklace"] = check_collected_item(necklace, "necklace", uncollected_items, dic_items["collected_necklace"], dic_items["not_collected_necklace"])

            belt = item_image_grab(1, 2, 1)
            uncollected_items, dic_items["not_collected_belt"] = check_collected_item(belt, "belt", uncollected_items, dic_items["collected_belt"], dic_items["not_collected_belt"])

            ring = item_image_grab(2, 2, 1)
            uncollected_items, dic_items["not_collected_ring"] = check_collected_item(ring, "ring", uncollected_items, dic_items["collected_ring"], dic_items["not_collected_ring"])

            talisman = item_image_grab(3, 2, 1)
            uncollected_items, dic_items["not_collected_talisman"] = check_collected_item(talisman, "talisman", uncollected_items, dic_items["collected_talisman"], dic_items["not_collected_talisman"])

            print("Uncollected items: {}".format(uncollected_items))
            if uncollected_items >= min_uncollected_items_to_attack:
                return dic_items

    return dic_items


# =============================================================================
# START
# =============================================================================
print("STARTING NEW RUN")
time.sleep(3)
# wait for switch in the game window and click to search bar
a = 0
start_time = 0
while a < max_no_attacks:
    print("Attack number: {}".format(a))
    a += 1
    dic_items = search(dic_items)
    while time.time() - start_time <= 605:
        time.sleep(5)
    dic_items = attack_and_store(dic_items)
    time.sleep(1)
    start_time = time.time()


print("DONE")
print("Total unique HELMET: {}".format(len(not_collected_helmet)))
print("Total unique CHEST: {}".format(len(not_collected_chest)))
print("Total unique GLOVES: {}".format(len(not_collected_gloves)))
print("Total unique BOOTS: {}".format(len(not_collected_boots)))
print("Total unique WEAPON: {}".format(len(not_collected_weapon)))
print("Total unique NECKLACE: {}".format(len(not_collected_necklace)))
print("Total unique BELT: {}".format(len(not_collected_belt)))
print("Total unique RING: {}".format(len(not_collected_ring)))
print("Total unique TALISMAN: {}".format(len(not_collected_talisman)))

print("Total unique ALL: {}".format(
    len(not_collected_helmet) +
    len(not_collected_chest) +
    len(not_collected_gloves) +
    len(not_collected_boots) +
    len(not_collected_weapon) +
    len(not_collected_necklace) +
    len(not_collected_belt) +
    len(not_collected_ring) +
    len(not_collected_talisman)
))

# =============================================================================
# END OF FILE
# =============================================================================

