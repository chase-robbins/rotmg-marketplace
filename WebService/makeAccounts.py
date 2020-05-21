from pynput.mouse import Controller as m1
from pynput.mouse import Button
from pynput.keyboard import Controller as k1
from pynput.keyboard import Key
import random
import string
import math
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import DBManager
import time

mouse = m1()
keyboard = k1()
startingDot = 2
engine = create_engine('postgresql://postgres:testingPassword@localhost/postgres', echo = True)
conn = engine.connect()

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def emailgen():
    file = open('file.txt', 'r+')
    newInt = int(str(file.readlines()[0])) + 1
    email = "chaserobbinsyt@gmail.com"
    with open('file.txt', 'w') as file:
        file.writelines( str(newInt) )
    return "rotmgmules69420+" + str(newInt-1) + "@gmail.com"

smallwait = 0.5

def checkRepeats(pw):
    testChar = ""
    for element in pw:
        if element == testChar:
            return True
            print("CheckRepeats detected a repeating character.")
        testChar = element
    print("CheckRepeats succeeded. No repeats detected.")
    return False

y=0
while y !=10:
    x=0
    while x != 24:
        name = randomString(10)
        email = emailgen()
        pw = randomString(9) + "1"
        while checkRepeats(pw) == True:
            pw = randomString(9) + "1"
            print("Detected repeat. Creating new password.")
        month = 5
        day = 5
        year = random.randint(1990,2002)

        mouse.position = (-803,671)
        mouse.click(Button.left,1)
        time.sleep(smallwait)
        #type name
        mouse.position = (-829,360)
        mouse.click(Button.left,1)
        time.sleep(smallwait)
        keyboard.type(name)
        time.sleep(smallwait)
        #type email
        mouse.position = (-903,408)
        mouse.click(Button.left,1)
        time.sleep(smallwait)
        keyboard.type(email)
        time.sleep(smallwait)
        #type pw1
        mouse.position = (-891,450)
        mouse.click(Button.left,1)
        time.sleep(smallwait)
        keyboard.type(pw)
        time.sleep(smallwait)
        #type pw2
        mouse.position = (-841,501)
        mouse.click(Button.left,1)
        time.sleep(smallwait)
        keyboard.type(pw)
        time.sleep(smallwait)
        #type mon
        # mouse.position = (-950,545)
        # mouse.click(Button.left,1)
        # time.sleep(smallwait)
        # keyboard.type(str(month))
        # time.sleep(smallwait)
        # #type day
        # mouse.position = (-861,542)
        # mouse.click(Button.left,1)
        # time.sleep(smallwait)
        # keyboard.type(str(day))
        # time.sleep(smallwait)
        #type year
        mouse.position = (-762,544)
        mouse.click(Button.left,1)
        time.sleep(smallwait)
        keyboard.type(str(year))
        time.sleep(smallwait)
        #click register
        mouse.position = (-777, 671)
        mouse.click(Button.left,1)
        time.sleep(5)
        #click log out
        mouse.position = (-1008, 596)
        mouse.click(Button.left,1)
        time.sleep(smallwait)
        i = DBManager.mules.insert().values(IGN = name, Email = email, Password = pw, bdayMonth = month, bdayDay = day, bdayYear = year, slot1 = 0, slot2 = 0, slot3 = 0, slot4 = 0, slot5 = 0, slot6 = 0, slot7 = 0, slot8 = 0, slot9 = 0, slot10 = 0, slot11 = 0, slot12 = 0, slot13 = 0, slot14 = 0, slot15 = 0, slot16 = 0)
        result = conn.execute(i)
        x+=1
        print("x=" + str(x))
        print("Account Created. Details Below:")
        print("Username: " + name)
        print("Password: " + pw)
        print("Birthday: " + str(day) + " " + str(month) + " " + str(year))
    mouse.position(-1647,222)
    mouse.click(Button.left,1)
    mouse.position(-1451,580)
    mouse.click(Button.left,1)
    mouse.position(-1612,214)
    mouse.click(Button.left,1)
    y+=1
    print("y=" + str(y))
    print("sleeping for 15 sec")
    time.sleep(15)
    print("back up")

#create engine for SQLAlchemy ORM
