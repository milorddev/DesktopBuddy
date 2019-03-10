from tkinter import *
import time
import os
import random
import math
import win32_windows as win

imageIndex = 0
coords = {'x':0, 'y':0}
prevCoords = {'x':0, 'y':0}
yVelocity = 0
flippedAnim = False
keyObj = {'a':False, 's':False, 'd':False, 'w':False}
dist = 6
interpVal = 0
jumpTrigger = True
refreshRate = 32

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
    root.after(math.ceil(refreshRate * 1.618), animUpdate, flippedAnim)

#check the bounding box first, then apply the movement
def applyPosition(xOverride=0, yOverride=0):
    global coords, prevCoords, jumpTrigger
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

    detectPlatforms()

    prevCoords = coords
    coords = {'x':boundX+xOverride, 'y':boundY+yOverride}
    root.geometry("+" + str(coords['x']) + "+" + str(coords['y']))



def detectPlatforms():
    global coords, prevCoords, jumpTrigger
    wins = win.get_windows()
    #character position, before and current
    xPos = (prevCoords['x']+8, coords['x']+8)
    yPos = (prevCoords['y']+32, coords['y']+32)
    
    for i in wins:
        ends = (i['topleft'][0], i['topleft'][0] + i['width'])
        y = i['topleft'][1]

        if xPos[0] < ends[0] and xPos[1] < ends[0]: #if before the left x of the platform, skip
            continue
        elif xPos[0] > ends[1] and xPos[1] > ends[1]: # if after the right x of the platform, skip
            continue
        elif y >= yPos[0] and y <= yPos[1]: #we are in the Yrange, make him stand!
            jumpTrigger = False
            

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

def lerp(steps, updown): #eg. 32 steps to get from 0 to 6
    global interpVal
    if updown == 'up':
        interpVal = dist/steps + interpVal if dist/steps + interpVal < dist else dist
    else:
        interpVal = interpVal - dist/steps if interpVal - dist/steps > 0 else 0
    #print(interpVal)
    return math.ceil(interpVal)

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
            yVelocity = -20
            jumpTrigger = True
    if charkey == 's' or charkey == 'S':
        keyObj['s'] = True

def moveLoop():
    global currentAnim, yVelocity, interpVal
    if root.focus_get() == None:
        print('do nothing, not focused')
    else:
        for i in keyObj:
            if i == 'a' and keyObj[i] == True:
                moveLeft(lerp(8,'up'))
            if i == 's' and keyObj[i] == True:
                pass
            if i == 'd' and keyObj[i] == True:
                moveRight(lerp(8,'up'))
            if i == 'w' and keyObj[i] == True:
                moveUp(lerp(8,'up'))

        if jumpTrigger == True:
            currentAnim = jumping
            moveDown(yVelocity)
        else:
            if keyObj['w'] == False and keyObj['a'] == False and keyObj['s'] == False and keyObj['d'] == False:
                currentAnim = idle
                interpVal = 0
            if keyObj['s'] == True:
                currentAnim = crouching
                interpVal = 0
            elif keyObj['a'] == True or keyObj['d'] == True:
                currentAnim = running
                
        applyPosition()
        yVelocity += 2
    root.after(refreshRate,moveLoop)

root = Tk()

idle = (animArray(False,'idle.gif'), animArray(True, 'idle_Flipped.gif'))
running = (animArray(False,'running.gif'), animArray(True, 'running_Flipped.gif'))
jumping = (animArray(False,'jumping.gif'), animArray(True, 'jumping_Flipped.gif'))
crouching = (animArray(False,'crouching.gif'), animArray(True, 'crouching_Flipped.gif'))
#skidding = (animArray(False,'skidding.gif'), animArray(True, 'skidding_Flipped.gif'))

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
root.after(refreshRate,moveLoop)
root.mainloop()
