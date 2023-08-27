import sys
import random
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QMainWindow
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtMultimedia import QSound

class Pet(QWidget):
    def __init__(self) -> None:
        super().__init__()

        # Get screen dimensions
        screen = QApplication.primaryScreen().geometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()

        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow
        )
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.repaint()

        self.layout = QHBoxLayout(self)
        
        self.image = QLabel(self)
        self.ims = self.loadIms('images/pet_02')
        self.imIndex = 0
        self.setImage(self.ims[self.imIndex])
        self.layout.addWidget(self.image)
        
        self.message_label = QLabel(self)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("background-color: white; border-radius: 5px;")
        
        font = QFont()
        font.setPointSize(14)
        self.message_label.setFont(font)
        
        self.layout.addWidget(self.message_label)
        
        self.setLayout(self.layout)
        
        self.resize(128, 128)
        self.move(100, 200)
        self.show()
        
        self.follow_mouse = False
        self.timer = QTimer(self)
        self.startTimer()
        
        self.message_timer = QTimer(self)
        self.message_timer.timeout.connect(self.showMessage)
        self.message_timer.start(33000)

        self.changeMessageTimer = 3600
    
    def loadIm(self, im_path):
        im = QImage()
        im.load(im_path)
        return im
    
    def loadIms(self, ims_path):
        return [self.loadIm(f'{ims_path}/shime{i}.png') for i in range(1, 53)]
    
    def setImage(self, image):
        self.image.setPixmap(QPixmap.fromImage(image))
    
    def startTimer(self):
        self.timer.timeout.connect(self.nextFrame)
        self.timer.start(500)
    
    def nextFrame(self):
        self.changeMessageTimer -= 1
        self.imIndex += 1
        if self.imIndex > 51:
            self.imIndex = 0
        self.setImage(self.ims[self.imIndex])

    def showMessage(self):
        messages = ["I'm Raiden Shogun", "此刻，寂灭之时!", "I love Tricolor Dango", "Where's Yae", "Don't make me cook"]
        urgent_messages = ["You need to rest", "You are using computer for too long"]

        if self.changeMessageTimer <= 0:
            messages.extend(urgent_messages)

        message_index = random.randint(0, len(messages)-1)
        selected_message = messages[message_index]


        if selected_message in urgent_messages:
            self.message_label.setStyleSheet("background-color: red; color: white; border-radius: 5px;")
        else:
            self.message_label.setStyleSheet("background-color: white; color: black; border-radius: 5px;")

        self.message_label.setText(selected_message)
        self.message_label.show()
        self.message_timer.singleShot(3000, self.hideMessage)

    def hideMessage(self):
        # Reset the style to default when hiding the message
        self.message_label.setStyleSheet("background-color: white; color: black; border-radius: 5px;")
        self.message_label.hide()

    def mousePressEvent(self, event):
        button = event.button()
        if button == Qt.LeftButton:
            self.follow_mouse = True

            a = random.randint(1, 2)
            self.sound = QSound("images/pet_02/sound/" + str(a) + ".wav")
            self.sound.play()
            
            event.accept()
        elif button == Qt.RightButton:
            self.close()
            sys.exit()

    def mouseMoveEvent(self, event):
        if self.follow_mouse:
            x = event.globalX() - self.width() // 2   # Get the center of the widget
            y = event.globalY() - self.height() // 2  # Get the center of the widget
            
            # Ensure the window does not exceed the screen boundaries
            x = max(0, min(self.screen_width - self.width(), x))
            y = max(0, min(self.screen_height - self.height(), y))
            
            self.move(x, y)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.follow_mouse = False

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setGeometry(100, 100, 400, 400)
        self.show()

app = QApplication(sys.argv)
pet = Pet()
sys.exit(app.exec_())
