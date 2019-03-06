from tkinter import *
import time
import os
import random

imageIndex = 0
coords = {'x':0, 'y':0}
yVelocity = 0
flippedAnim = False
keyObj = {'a':False, 's':False, 'd':False, 'w':False}
dist = 2
jumpTrigger = True

#get an array of individual slides for a full animation
def animArray(flipped,fpath):
    anim = []
    index = 0
    while True:
        form = "gif -index " + str(index)
        try:
            #if(flipped):
                #anim.append(PhotoImage(file=fpath, format=form))
            #else:
            photo = PhotoImage(file=fpath, format=form)
            photo = photo.zoom(2,2)
            anim.append(photo)
            index += 1
        except:
            break;
    return anim

#gets the next frame for the animation, if last frame, loop to first
def animNextFrame(animation):
    global imageIndex;
    try:
        test = animation[imageIndex + 1]
        imageIndex = imageIndex + 1
        return test
    except:
        imageIndex = 0
        return animation[0]

#updates the animation, keep coords in bounds
def animUpdate(flipped):
    global coords, boundingBox;
    if(flipped):
        frame = animNextFrame(currentAnim[1])
    else:
        frame = animNextFrame(currentAnim[0])
    label.configure(image=frame)
    root.after(64, animUpdate, flippedAnim)

#check the bounding box first, then apply the movement
def applyPosition():
    global coords, jumpTrigger
    boundX = coords['x']
    if coords['x'] < boundingBox['left']:
        boundX = boundingBox['left']
    elif coords['x'] > boundingBox['right']:
        boundX = boundingBox['right']

    boundY = coords['y']
    if coords['y'] < boundingBox['top']:
        boundY = boundingBox['top']
    elif coords['y'] > boundingBox['bottom']:
        boundY = boundingBox['bottom']
        jumpTrigger = False

    coords = {'x':boundX, 'y':boundY}
    root.geometry("+" + str(coords['x']) + "+" + str(coords['y']))



#moving left by 1 pixel
def moveLeft(num):
    global coords, flippedAnim;
    coords['x'] -= num;
    flippedAnim = True

#moving right by 1 pixel
def moveRight(num):
    global coords, flippedAnim;
    coords['x'] += num;
    flippedAnim = False

#moving up by 1 pixel
def moveUp(num):
    global coords;
    coords['y'] -= num;


#moving down by 1 pixel
def moveDown(num):
    global coords;
    coords['y'] += num;
    

def keyup(e):
    global keyObj
    charkey = e.char
    if charkey == 'a' or charkey == 'A':
        keyObj['a'] = False
    if charkey == 'd' or charkey == 'D':
       keyObj['d'] = False
    if charkey == 'w' or charkey == 'W':
        keyObj['w'] = False
    if charkey == 's' or charkey == 'S':
        keyObj['s'] = False
    
def keydown(e):
    global keyObj, jumpTrigger, yVelocity
    charkey = e.char
    if charkey == 'a' or charkey == 'A':
        keyObj['a'] = True
    if charkey == 'd' or charkey == 'D':
       keyObj['d'] = True
    if charkey == 'w' or charkey == 'W':
        #keyObj['w'] = True
        if jumpTrigger == False:
            yVelocity = -15
            jumpTrigger = True
    if charkey == 's' or charkey == 'S':
        keyObj['s'] = True

def moveLoop():
    global currentAnim, yVelocity
    for i in keyObj:
        if i == 'a' and keyObj[i] == True:
            moveLeft(dist)
        if i == 's' and keyObj[i] == True:
            moveDown(dist)
        if i == 'd' and keyObj[i] == True:
            moveRight(dist)
        if i == 'w' and keyObj[i] == True:
            moveUp(dist)

    if jumpTrigger == True:
        currentAnim = jumping
        moveDown(yVelocity)
        print(yVelocity)
    else:
        if keyObj['w'] == False and keyObj['a'] == False and keyObj['s'] == False and keyObj['d'] == False:
            currentAnim = idle
        if keyObj['a'] == True or keyObj['d'] == True:
            currentAnim = running
        
    applyPosition()
    yVelocity += 1
    root.after(32,moveLoop)

root = Tk()

idle = (animArray(False,'idle.gif'), animArray(True, 'idle_Flipped.gif'))
running = (animArray(False,'running.gif'), animArray(True, 'running_Flipped.gif'))
jumping = (animArray(False,'jumping.gif'), animArray(True, 'jumping_Flipped.gif'))
crouching = (animArray(False,'crouching.gif'), animArray(True, 'crouching_Flipped.gif'))
skidding = (animArray(False,'skidding.gif'), animArray(True, 'skidding_Flipped.gif'))

currentAnim = idle

label = Label(root, bg='white')
boundingBox = {'left': 0, 'right': root.winfo_screenwidth() - 40, 'top': 0, 'bottom': root.winfo_screenheight() - 100}

#keyboard binding
label.bind("<KeyPress>", keydown)
label.bind("<KeyRelease>", keyup)

root.overrideredirect(True)
root.lift()
root.geometry("+" + str(coords['x']) + "+" + str(coords['y']))
root.wm_attributes("-topmost", True)
#root.wm_attributes("-disabled", True)
root.wm_attributes("-transparentcolor", "white")


label.pack()
label.focus_set()
root.after(0, animUpdate, flippedAnim)
root.after(32,moveLoop)
root.mainloop()
