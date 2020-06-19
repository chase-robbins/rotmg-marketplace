from pynput.mouse import Controller as m1
from pynput.mouse import Button
from pynput.keyboard import Controller as k1
from pynput.keyboard import Key
import time
mouse = m1()
keyboard = k1()
x=0
while x != 8:
    mouse.position = (1776,192)
    time.sleep(1)
    mouse.click(Button.left,1)
    time.sleep(1)
    keyboard.pressed(Key.ctrl)
    time.sleep(1)
    mouse.position = (1100,837)
    time.sleep(1)
    mouse.click(Button.left,1)
    time.sleep(1)
    # mouse.position = (641,290)
    # mouse.click(Button.left,1)
    # time.sleep(1)
    # keyboard.pressed(Key.ctrl)
    # mouse.position = (1100,837)
    # mouse.click(Button.left,1)
    # keyboard.release(Key.ctrl)
    # time.sleep(1)
    # mouse.position = (1617,16)
    # mouse.click(Button.left,1)
    # time.sleep(120)
    # mouse.position = (1189,17)
    # mouse.click(Button.left,1)
    # time.sleep(0.5)
    # mouse.position = (432,187)
    # mouse.click(Button.left,1)
    # time.sleep(1)
    x+=1
    print(str(x))
