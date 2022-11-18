from PyQt5.QtCore import QDateTime, Qt, QTimer
from PySide6.QtWidgets import QApplication
from PyQt5.QtGui import QImage, QPixmap

from PyQt5.QtWidgets import (QApplication,
        QGridLayout, QGroupBox, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy,
        QWidget)
import sys
from glob import glob
import os

class ImageScreen(QWidget):
    def __init__(self, parent=None, folder=None):
        super(ImageScreen, self).__init__(parent)
        self.parent = parent
        self.folder = folder

        self.originalPalette = QApplication.palette()
        self.imageLabelScale = 0.5
        self.resize(1920, 1000)

        self.createImagePane()
        self.createControlPane()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.imageLabel, 0, 0, 20, 1)
        mainLayout.addWidget(self.controlPane, 21, 0, 1, 1)
        self.setLayout(mainLayout)


    def createImagePane(self):
        # self.gb = QGroupBox("image pane")
        self.imageLabel = QLabel()
        # self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.resize(int(1920 * self.imageLabelScale), int(1080 * self.imageLabelScale))

        self.image_list = glob(os.path.join(self.folder, "*.png"))
        self.current_image = 0
        image = QImage(self.image_list[self.current_image])
        self.imageLabel.setPixmap(QPixmap.fromImage(image))
        self.imageLabel.resize(int(1920 * self.imageLabelScale), int(1080 * self.imageLabelScale))






    def createControlPane(self):
        self.controlPane = QGroupBox()
        self.nextButton = QPushButton('>')
        self.nextButton.clicked.connect(self.changeImage)
        self.previousButton = QPushButton('<')
        self.previousButton.clicked.connect(self.changeImage)

        layout = QHBoxLayout()
        layout.addWidget(self.previousButton)
        layout.addWidget(self.nextButton)

        self.controlPane.setLayout(layout)

    def changeImage(self, i=1):
        self.current_image = (self.current_image+1)%(len(self.image_list))
        image = QImage(self.image_list[self.current_image])
        self.imageLabel.setPixmap(QPixmap.fromImage(image))

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     screen = ImageScreen()
#     screen.show()
#     sys.exit(app.exec())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    widget = ImageScreen(window)
    window.show()

    sys.exit(app.exec())