from tkinter import *
import time
import os
import random

imageIndex = 0
coords = {'x':0, 'y':0}
mouseStart = {'x':0, 'y':0}
mouseVelocity = {'x':0, 'y':0}
previousMouse = {'x':0, 'y':0}
flippedAnim = False

#get an array of individual slides for a full animation
def animArray(flipped):
    anim = []
    index = 0
    while True:
        form = "gif -index " + str(index)
        try:
            if(flipped):
                anim.append(PhotoImage(file='Chimecho_XY_Flipped.gif', format=form))
            else:
                anim.append(PhotoImage(file='Chimecho_XY.gif', format=form))
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
        frame = animNextFrame(framesFlipped)
    else:
        frame = animNextFrame(frames)
    label.configure(image=frame)
    root.after(32, animUpdate, flippedAnim)

#check the bounding box first, then apply the movement
def applyPosition():
    global coords
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

    coords = {'x':boundX, 'y':boundY}
    root.geometry("+" + str(coords['x']) + "+" + str(coords['y']))

#alternative for loop working with tkinter's mainloop thing. takes in the count and whatever function stack you want
def loopFunc(count, funcList, endFunc):
    if count <= 0:
        endFunc()
    else:
        for i in funcList:
            i[0](i[1])
        root.after(32,loopFunc, count-1, funcList, endFunc)

#blank after loop function
def printEnd():
    print('end')

#mouse left click
def leftMouseStart(e):
    global mouseStart;
    mouseStart = {'x':e.x, 'y':e.y}

#you can drag him around, and the velocity of him will be calculated for when he is thrown
def leftMouseHeld(e):
    global mouseVelocity, previousMouse, coords
    newX = e.x_root - mouseStart['x']
    newY = e.y_root - mouseStart['y']
    mouseVelocity = {'x':(newX - previousMouse['x'])*3, 'y': (newY - previousMouse['y'])*3}
    coords = {'x':newX, 'y':newY}
    previousMouse = {'x':newX, 'y':newY}
    print(mouseVelocity)
    applyPosition()

#calculate the residual velocity and slow down to stop
def leftMouseEnd(e):
    global mouseVelocity, coords
    tracker = max([abs(mouseVelocity['x']), abs(mouseVelocity['y'])])
    if round(tracker) > 1:
        tracker = tracker/1.61
        mouseVelocity = {'x':round(mouseVelocity['x']/1.61), 'y': round(mouseVelocity['y']/1.61)}
        coords = {'x': coords['x'] + mouseVelocity['x'] , 'y': coords['y'] + mouseVelocity['y']}
        applyPosition()
        root.after(32,leftMouseEnd, e)
    print(e)

#mouse right click
def rightMouseStart(e):
    mouseStart = {'x':e.x, 'y':e.y}

#nothing on right drag
#def rightMouseHeld(e):
    #print(e)

#start the move to coordinates
def rightMouseEnd(e):
    newX = e.x_root - mouseStart['x']
    newY = e.y_root - mouseStart['y']
    pathToCoord(newX, newY, printEnd)

#moving left by 1 pixel
def moveLeft(num):
    global coords, flippedAnim;
    coords['x'] -= num;
    applyPosition()
    flippedAnim = False

#moving right by 1 pixel
def moveRight(num):
    global coords, flippedAnim;
    coords['x'] += num;
    applyPosition()
    flippedAnim = True

#moving up by 1 pixel
def moveUp(num):
    global coords;
    coords['y'] -= num;
    applyPosition()

#moving down by 1 pixel
def moveDown(num):
    global coords;
    coords['y'] += num;
    applyPosition()

#find x and y amounts in order to path over to that coordinate
def pathToCoord(destX, destY, endFunc):
    global coords
    diffX = destX - coords['x']
    diffY = destY - coords['y']
    funcList = []

    print(diffX, diffY)

    if diffX != 0 and diffY != 0:  #both diffX and diffY has a value other than 0
        xFunc = moveLeft if diffX < 0 else moveRight
        yFunc = moveUp if diffY < 0 else moveDown

        if abs(diffX) > abs(diffY):  #x is bigger
            print('x is bigger')
            lower = round(diffY/diffX)
            loopFunc(abs(diffX),[(xFunc,1), (yFunc,lower)], endFunc)
        elif abs(diffX) < abs(diffY):  #y is higher
            print('y is bigger')
            lower = round(diffX/diffY)
            loopFunc(abs(diffY),[(xFunc,lower), (yFunc,1)], endFunc)
        else:  #both are equal
            print('both are equal')
            loopFunc(abs(diffX),[(xFunc,1), (yFunc,1)], endFunc)

    else:  #one of them are 0
        if diffX == 0:  #only move y direction
            print('only move y directio')
            yFunc = moveUp if diffY < 0 else moveDown
            loopFunc(abs(diffY),[(yFunc,1)], endFunc)
        elif diffY == 0:  #only move x direction
            print('only move x directio')
            xFunc = moveLeft if diffX < 0 else moveRight
            loopFunc(abs(diffX),[(xFunc,1)], endFunc)
        else:  #same spot
            print('same spot')


def path():
    time.sleep(random.randrange(0,10))
    print('path')
    newX = random.randrange(boundingBox['left'],boundingBox['right'])
    newY = random.randrange(boundingBox['top'],boundingBox['bottom'])
    pathToCoord(newX, newY, path)


root = Tk()
frames = animArray(False)
framesFlipped = animArray(True)
label = Label(root, bg='white')
boundingBox = {'left': 0, 'right': root.winfo_screenwidth() - 40, 'top': 0, 'bottom': root.winfo_screenheight() - 100}

#mouse bindings
label.bind("<Button-1>", leftMouseStart)
label.bind("<B1-Motion>", leftMouseHeld)
label.bind("<ButtonRelease-1>", leftMouseEnd)

label.bind("<Button-3>", rightMouseStart)
#label.bind("<B3-Motion>", rightMouseHeld)
label.bind("<ButtonRelease-3>", rightMouseEnd)


root.overrideredirect(True)
root.lift()
root.geometry("+" + str(coords['x']) + "+" + str(coords['y']))
root.wm_attributes("-topmost", True)
#root.wm_attributes("-disabled", True)
root.wm_attributes("-transparentcolor", "white")


label.pack()
root.after(0, animUpdate, flippedAnim)
root.after(32,path)
root.mainloop()
