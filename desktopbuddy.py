from tkinter import *
import time
import os

imageIndex = 0
coords = {'x':0, 'y':0}

#get an array of individual slides for a full animation
def animArray():
    anim = []
    index = 0
    while True:
        form = "gif -index " + str(index)
        try:
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

#updates the animation
def animUpdate():
    frame = animNextFrame(frames)
    label.configure(image=frame)
    root.after(32, animUpdate)

#alternative for loop working with tkinter's mainloop thing. takes in the count and whatever function stack you want
def loopFunc(count, funcList):
    if count <= 0:
        print('end')
    else:
        for i in funcList:
            i[0](i[1])
        root.after(32,loopFunc, count-1, funcList) 

#moving left by 1 pixel
def moveLeft(num):
    global coords;
    coords['x'] -= num;
    root.geometry("+" + str(coords['x']) + "+" + str(coords['y']))

#moving right by 1 pixel
def moveRight(num):
    global coords;
    coords['x'] += num;
    root.geometry("+" + str(coords['x']) + "+" + str(coords['y']))

#moving up by 1 pixel
def moveUp(num):
    global coords;
    coords['y'] -= num;
    root.geometry("+" + str(coords['x']) + "+" + str(coords['y']))

#moving down by 1 pixel
def moveDown(num):
    global coords;
    coords['y'] += num;
    root.geometry("+" + str(coords['x']) + "+" + str(coords['y']))


def pathToCoord(destX, destY):
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
            loopFunc(abs(diffX),[(xFunc,1), (yFunc,lower)])
        elif abs(diffX) < abs(diffY):  #y is higher
            print('y is bigger')
            lower = round(diffX/diffY)
            loopFunc(abs(diffY),[(xFunc,lower), (yFunc,1)])
        else:  #both are equal
            print('both are equal')
            loopFunc(abs(diffX),[(xFunc,1), (yFunc,1)])

    else:  #one of them are 0
        if diffX == 0:  #only move y direction
            print('only move y directio')
            yFunc = moveUp if diffY < 0 else moveDown
            loopFunc(abs(diffY),[(yFunc,1)])
        elif diffY == 0:  #only move x direction
            print('only move x directio')
            xFunc = moveLeft if diffX < 0 else moveRight
            loopFunc(abs(diffX),[(xFunc,1)])
        else:  #same spot
            print('same spot')


def path():
    #loopFunc(300,[(moveLeft,1), (moveUp,1)])
    #pathToCoord(500,500)
    pathToCoord(350,250)
    pathToCoord(500,100)


root = Tk()
frames = animArray()
label = Label(root, bg='white')

root.overrideredirect(True)
root.lift()
root.geometry("+" + str(coords['x']) + "+" + str(coords['y']))
root.wm_attributes("-topmost", True)
root.wm_attributes("-disabled", True)
root.wm_attributes("-transparentcolor", "white")


label.pack()
root.after(0, animUpdate)
root.after(32,path)
root.mainloop()
