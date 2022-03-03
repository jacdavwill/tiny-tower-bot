from pynput import keyboard
from pynput.keyboard import Key, Controller
import pyautogui
from random import randint, uniform
from time import sleep as sleeper

# random
keyboard_input = Controller()
alphabet = ['b', 'c', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'n', 'o', 'p', 'q', 'r', 'u', 'v']
mouse_movements = [pyautogui.easeOutExpo, pyautogui.easeOutBounce, pyautogui.easeOutCirc, pyautogui.easeInBounce,
                   pyautogui.easeInExpo]
background_color = (14, 32, 41)
backpack_pos_1 = (3646, 559)
backpack_slots = []
for y in range(7):
    for x in range(4):
        backpack_slots.append((backpack_pos_1[0] + x * 54, backpack_pos_1[1] + y * 45))

def get_color():
    def get_key_name(key):
        if isinstance(key, keyboard.KeyCode):
            return key.char
        else:
            return str(key)


    check_pos = [3646, 559]
    delta = 5
    def on_press(key):
        global delta
        key_name = get_key_name(key)
        # print('Key {} pressed.'.format(key_name))
        if key_name == "Key.right":
            check_pos[0] += delta
            # print()
        elif key_name == "Key.left":
            check_pos[0] -= delta
            # print()
        elif key_name == "Key.down":
            check_pos[1] += delta
        elif key_name == "Key.up":
            check_pos[1] -= delta
        elif key_name == "Key.space":
            delta = 1 if delta == 5 else 5

    listener = keyboard.Listener(on_press=on_press)
    listener.start()


def click(key="mouse"):
    if key == "mouse":
        # print("clicking")
        pyautogui.click()
    else:
        # print("pressing " + str(key))
        keyboard_input.press(key)
        keyboard_input.release(key)


def nav_box(box):
    dur = uniform(.25, .75)
    pos = (randint(box[0][0], box[1][0]), randint(box[1][1], box[0][1]))
    pyautogui.moveTo(pos[0], pos[1], dur, mouse_movements[randint(0, 4)])
    sleeper(dur)
    keyboard_input.press(Key.ctrl)
    sleep(.1, .2)
    click()
    keyboard_input.release(Key.ctrl)


def nav_pt(pos):
    dur = uniform(.25, .75)
    pyautogui.moveTo(pos[0], pos[1], dur, mouse_movements[randint(0, 4)])
    sleeper(dur)
    keyboard_input.press(Key.ctrl)
    sleep(.1, .2)
    click()
    keyboard_input.release(Key.ctrl)


def get_items():
    num = 0
    threshold = 18
    for slot in backpack_slots:
        current_color = pyautogui.pixel(slot[0], slot[1])
        if abs((current_color[0] - background_color[0])) > threshold or \
                abs((current_color[1] - background_color[1])) > threshold or \
                abs((current_color[2] - background_color[2])) > threshold:
            num += 1
    return num


def empty_backpack():
    print("emptying backpack")
    sleep(.5, 1)
    keyboard_input.press(Key.space)
    keyboard_input.release(Key.space)
    sleep(.5, 1)
    for x in range(randint(10, 15)):
        if uniform(0, 1) < .5:
            keyboard_input.press('2')
            keyboard_input.release('2')
        else:
            keyboard_input.press('1')
            keyboard_input.release('1')
        sleep(.1, .2)


def press_random_letter():
    letter = alphabet[randint(0, 15)]
    keyboard_input.press(letter)
    keyboard_input.release(letter)
    sleep(.5, .7)
    # keyboard_input.press('b')
    # keyboard_input.release('b')


def sleep(x, y):
    sleeper(uniform(x, y))


def fishing():
    # stand in southernmost fishing spot of the 3 in barb vill - bank preset 1 has 27 feathers is banking, otherwise,
    # carry all. Toolbar presets 1 - drop raw trout 2- drop raw salmon. Bank preset 1 - 50 feathers
    trans_up_low = (2763, 377)
    trans_up_high = (2824, 318)
    trans_down_low = (2763, 586)
    trans_down_high = (2824, 528)
    trans_double_up_low = (2763, 260)
    trans_double_up_high = (2824, 234)
    trans_double_down_low = (2763, 716)
    trans_double_down_high = (2824, 665)
    last_position = 0
    position = 0
    max_pos = 2

    def move_double_down():
        print("moving double down")
        pos = (randint(trans_double_down_low[0], trans_double_down_high[0]),
               randint(trans_double_down_high[1], trans_double_down_low[1]))
        pyautogui.moveTo(pos[0], pos[1], uniform(.25, .75), mouse_movements[randint(0, 4)])

    def move_double_up():
        print("moving double up")
        pos = (randint(trans_double_up_low[0], trans_double_up_high[0]),
               randint(trans_double_up_high[1], trans_double_up_low[1]))
        pyautogui.moveTo(pos[0], pos[1], uniform(.25, .75), mouse_movements[randint(0, 4)])

    def move_down():
        global last_position
        global position
        top_bound = 3 if last_position == 1 else 1
        last_position = position
        if position - 2 >= 0 and (randint(0, 3) < top_bound) == 0:
            move_double_down()
            position -= 2
        else:
            print("moving down")
            pos = (randint(trans_down_low[0], trans_down_high[0]), randint(trans_down_high[1], trans_down_low[1]))
            pyautogui.moveTo(pos[0], pos[1], uniform(.25, .75), mouse_movements[randint(0, 4)])
            position -= 1

    def move_up():
        global last_position
        global position
        top_bound = 3 if last_position == 1 else 1
        last_position = position
        if position + 2 <= max_pos and (randint(0, 3) < top_bound) == 0:
            move_double_up()
            position += 2
        else:
            print("moving up")
            pos = (randint(trans_up_low[0], trans_up_high[0]), randint(trans_up_high[1], trans_up_low[1]))
            pyautogui.moveTo(pos[0], pos[1], uniform(.25, .75), mouse_movements[randint(0, 4)])
            position += 1

    def bank_run():
        tele = ((3058, 363), (3074, 348))
        varrok_tele = ((2764, 395), (2783, 378))
        waypt_1 = (2032, 39)
        banker = ((2408, 436), (2469, 374))
        waypt_3 = (1929, 359)
        waypt_4 = (2080, 211)
        print("bank run")
        click(Key.space)
        sleep(1, 1.5)
        click('t')
        sleep(1, 1.3)
        click('v')
        sleep(20, 25)
        nav_pt(waypt_1)
        sleep(45, 50)
        nav_box(banker)
        sleep(2, 2.5)
        click('1')
        sleep(1, 1.5)
        nav_pt(waypt_3)
        sleep(45, 50)
        nav_pt(waypt_4)
        sleep(30, 35)

    banking = False
    sleep(5)
    previous_items = get_items()
    items = get_items()
    while True:
        # print("Position: " + str(check_pos) + "    Color: " + str(pyautogui.pixel(check_pos[0], check_pos[1])))
        # sleep(1)
        if position == 0:
            move_up()
        elif position == max_pos:
            move_down()
        else:
            if randint(0, 3) < (3 if last_position == 0 else 1):
                move_up()
            else:
                move_down()
        print("position is " + str(position))
        pyautogui.click()
        press_random_letter()

        # fishing loop
        while True:
            if get_items() == 28 and not banking:
                bank_run()
                position = 0
                previous_items = get_items()
                items = get_items()
                break
            previous_items = get_items()
            print("previous_items: " + str(previous_items))
            sleep(randint(10, 15))
            # check that position is producing
            print("current items: " + str(get_items()))
            if get_items() <= previous_items:
                print("position is not producing")
                break
            print("position is producing")
            press_random_letter()
            if not banking:
                empty_backpack()


def crafting():
    # stand in lumbridge castle on the 3rd floor directly in front of bank with inventory full of flax
    waypt_5 = (274, 415) #(2140, 328)
    staircase = ((941, 619), (982, 583))  #((2655, 584), (2733, 508))
    spinning_wheel = ((1214, 370), (1226, 359)) #((3140, 108), (3186, 103))
    waypt_6 = ((649, 897), (700, 847)) #(2134, 302)
    waypt_7 = (310, 295) #(2167, 236)
    bank_booth = ((942, 478), (978, 460)) # ((2635, 356), (2727, 265))
    while True:
        # print(pyautogui.position())
        # sleep(1, 1)
        nav_pt(waypt_5)
        sleep(5, 6)
        nav_box(staircase)
        # press_random_letter()
        sleep(2, 3)
        nav_box(spinning_wheel)
        sleep(5, 7)
        click(Key.space)
        sleep(51, 54)
        # nav_pt(waypt_6)
        # press_random_letter()
        # sleep(4, 6)
        nav_box(waypt_6)#staircase)
        sleep(4, 6)
        # sleep(1, 1.3)
        click('1')
        sleep(1, 1.3)
        nav_pt(waypt_7)
        # press_random_letter()
        sleep(5, 6)
        nav_box(bank_booth)
        sleep(1, 1.4)
        click('2')
        sleep(1, 1.3)


def mining():
    position = 1
    waypt_1 = (2061, 42)
    banker = ((2771, 438), (2845, 381))
    waypt_2 = (2342, 514)
    waypt_3 = (2366, 355)
    ore_1 = ((2587, 653), (2654, 562))
    ore_2 = ((2766, 454), (2818, 396))
    sleep(5, 5)
    while True:
        # mining loop
        while get_items() != 28:
            if position == 1:
                nav_box(ore_1)
            else:
                nav_box(ore_2)
            sleep(1, 5)
            if get_items() > randint(6, 10):
                click('1')
                if position == 2:
                    nav_box(ore_1)
                    position = 1
                else:
                    nav_box(ore_2)
                    position = 2
        click('t')
        sleep(1, 1.3)
        click('v')
        sleep(18, 21)
        nav_pt(waypt_1)
        sleep(24, 26)
        nav_box(banker)
        sleep(1, 1.4)
        click('3')
        sleep(1, 1.3)
        click('1')
        sleep(1, 1.3)
        nav_pt(waypt_2)
        sleep(27, 29)
        nav_pt(waypt_3)
        sleep(23, 26)
        if uniform(0, 1) < .5:
            nav_box(ore_1)
            position = 1
        else:
            nav_box(ore_2)
            position = 2
        sleep(2, 2.5)


def smithing():
    furnace = ((927, 456), (1005, 385))
    while True:
        # print(pyautogui.position())
        # sleep(1, 1)
        nav_box(furnace)
        sleep(.8, 1)
        click('1')
        sleep(.8, 1)
        click(Key.space)
        sleep(49, 51)



def fletching():
    sleep(3, 3)
    while True:
        click('1')
        sleep(.8, 1)
        click(Key.space)
        sleep(9, 12)

# ore_2 = ((2766, 454), (2818, 396))
# sleep(5, 5)
# while True:
#     sleep(5, 5)
#     while True:
#         # mining loop
#         while get_items() != 28:
#             nav_box(ore_2)
#             sleep(1, 3)
#             if get_items() > randint(6, 10):
#                 click('1')
#                 nav_box(ore_2)


# from pynput import keyboard
#
#
# def on_press(key):
#     a = 1# do nothing
#
#
# action = 0
# def on_release(key):
#     global action
#     if key == keyboard.Key.esc:
#         # Stop listener
#         return False
#     elif key == keyboard.Key.space:
#         if action == 0:
#             pyautogui.click()
#             action += 1
#         else:
#             click('2')
#             action = (action + 1) % 3
#
# listener = keyboard.Listener(
#     on_press=on_press,
#     on_release=on_release)
# listener.start()
#
# while True:
#     a = 1
#     # do nothing

