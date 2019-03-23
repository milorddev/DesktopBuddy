import sys
import PySide2.QtWidgets as obj
import PySide2.QtGui as gui
import PySide2.QtCore as core

idle = ('anims/idle_Flipped.gif','anims/idle.gif')
running = ('anims/running_Flipped.gif','anims/running.gif')
jumping = ('anims/jumping_Flipped.gif','anims/jumping.gif')
crouching = ('anims/crouching_Flipped.gif','anims/crouching.gif')
skidding = ('anims/skidding_Flipped.gif','anims/skidding.gif')

anims = [idle, running, jumping, crouching, skidding]


class Actor(obj.QApplication):
    def __init__(self):
        self.body = obj.QLabel("Hello World")
        self.body.show()


'''
class Actor(obj.QLabel):
    def __init__(self, parent=None):
        super(Actor, self).__init__(parent)
        print('new actor made')
        self.changeAnims(running[1])
        self.show()

    def resizeAnims(self, img, percent):
        x = img.currentImage()
        pixmap = gui.QPixmap(x.scaledToWidth(50))
        
     
        return size.scaled(16, 32, core.Qt.AspectRatioMode.IgnoreAspectRatio)
    
    def changeAnims(self,animPath):
        img = gui.QMovie(animPath)        
        img.setScaledSize(self.resizeAnims(img,4))
        self.setMovie(img)
        img.start()

'''


if __name__ == '__main__':
    for i in range(0,3):
        actor = Actor()
        actor.exec_()


