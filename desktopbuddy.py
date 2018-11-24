from tkinter import *
import time
import os

imageIndex = 0
coords = {'x':1500, 'y':500}

#get an array of individual slides for a full animation
def animArray():
    anim = []
    index = 0
    while True:
        form = "gif -index " + str(index)
        try:
            anim.append(PhotoImage(file='C:/Users/Dreality/Pictures/Chimecho_XY.gif', format=form))
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


#def pathToCoord(destX, destY):
#    global coords
#    diffX = coords['x'] - destX
#    diffY = coords['y'] - destY
    

def path():
    loopFunc(300,[(moveLeft,1), (moveUp,1)])


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
