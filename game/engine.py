from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import multiprocessing
import sys

idle = ('anims/idle_Flipped.gif','anims/idle.gif')
running = ('anims/running_Flipped.gif','anims/running.gif')
jumping = ('anims/jumping_Flipped.gif','anims/jumping.gif')
crouching = ('anims/crouching_Flipped.gif','anims/crouching.gif')
skidding = ('anims/skidding_Flipped.gif','anims/skidding.gif')

anims = [idle, running, jumping, crouching, skidding]


class Actor(QWidget):
    def __init__(self, parent=None):
        super(Actor, self).__init__(parent)

        #properties
        self.activeDirection = {'up':False, 'down':False, 'left':False, 'right':False}
        
        #set position and window size
        #self.setPosition(100,100)
        
        #set the flags
        #self.setFlag(Qt.WindowType.SplashScreen)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        #setup Signals
        #self.
        self.layout = QVBoxLayout(self)
        self.body = QLabel('run new instance')
        self.body.setAttribute(Qt.WA_TranslucentBackground)
        self.setAnimation(idle[1])
        self.layout.addWidget(self.body)

    def resizeAnimation(self, animation):
        size = animation.scaledSize()
        return size.scaled(32, 64, Qt.AspectRatioMode.IgnoreAspectRatio)
    
    def setAnimation(self, animationPath):
        animation = QMovie(animationPath)
        animation.setScaledSize(self.resizeAnimation(animation))
        self.body.setMovie(animation)
        animation.start()

    def createDaemon(self):
        p = multiprocessing.Process(target=newActor)
        p.start()

    #event functions
    def focusInEvent(self, event):
        print('focused')

    def focusOutEvent(self, event):
        print('unfocused')


    #Key Events
    def keyPressEvent(self, event):
        self.processKeyEvent(event,'press')

    def keyReleaseEvent(self, event):
        self.processKeyEvent(event,'release')

    def processKeyEvent(self,event,etype):
        if event.key() == Qt.Key_A or event.key() == Qt.Key_Left:
            self.activeDirection['left'] = True if etype == 'press' else False
            
        if event.key() == Qt.Key_W or event.key() == Qt.Key_Up:
            self.activeDirection['up'] = True if etype == 'press' else False
            
        if event.key() == Qt.Key_D or event.key() == Qt.Key_Right:
            self.activeDirection['right'] = True if etype == 'press' else False
            
        if event.key() == Qt.Key_S or event.key() == Qt.Key_Down:
            self.activeDirection['down'] = True if etype == 'press' else False
        print(self.activeDirection)

    #Mouse Events
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print('left mouse press')
        elif event.button() == Qt.RightButton:
            print('right mouse press')
        else:
            print('other mouse button')

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            print('left mouse release')
        elif event.button() == Qt.RightButton:
            print('right mouse release')
        else:
            print('other mouse release')

    def mouseMoveEvent(self, event):
        pass
    

def newActor():
    app=QApplication(sys.argv)
    ex = Actor()
    ex.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    multiprocessing.set_start_method('spawn')
    app=QApplication(sys.argv)
    ex = Actor()
    ex.show()
    sys.exit(app.exec_())
