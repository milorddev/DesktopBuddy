import sys
from PySide2.QtWidgets import QApplication, QLabel
from PySide2.QtGui import QMovie, QKeySequence
from PySide2.QtCore import QTimer

idle = ('anims/idle_Flipped.gif','anims/idle.gif')
running = ('anims/running_Flipped.gif','anims/running.gif')
jumping = ('anims/jumping_Flipped.gif','anims/jumping.gif')
crouching = ('anims/crouching_Flipped.gif','anims/crouching.gif')
skidding = ('anims/skidding_Flipped.gif','anims/skidding.gif')

anims = [idle, running, jumping, crouching, skidding]






class Actor(QLabel):
    def __init__(self, parent=None):
        super(Actor, self).__init__(parent)
        print('new actor made')
        self.changeAnims(running[1])
        self.show()
    
    def changeAnims(self,animPath):
        img = QMovie(animPath)
        self.setMovie(img)
        img.start()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    actor = Actor()
    #the loop
    app.exec_()


