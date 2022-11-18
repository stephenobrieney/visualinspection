# from fbs_runtime.application_context.PyQt5 import ApplicationContext

import os
# import time
import sys
sys.path.append(os.getcwd())
# from frame_selection.main import main as fs_main

# from inference.main import image_pipeline

from app import main

from PySide6.QtWidgets import QApplication
from PyQt5.QtWidgets import (QApplication,
        QGroupBox, QLabel, QLineEdit,
         QPushButton, QStyleFactory, 
        QVBoxLayout, QWidget, QFileDialog)
import sys

from imageWidget import ImageScreen


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.originalPalette = QApplication.palette()
        self.resize(1920, 1080)

        self.createConfigScreen()
    
    def createConfigScreen(self):
        self.configScreen = ConfigScreen(self)

    def gotoImageViewer(self, folder):
        self.configScreen.setParent(None)
        self.imageViewer = ImageScreen(self, folder)
        self.imageViewer.setVisible(True)


class ConfigScreen(QWidget):
    def __init__(self, parent=None):
        super(ConfigScreen, self).__init__(parent)
        self.originalPalette = QApplication.palette()
        self.parent = parent

        self.createLeftGroupBox()
        self.createRightGroupBox()

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.left_gb)
        mainLayout.addWidget(self.right_gb)
        self.setLayout(mainLayout)

        QApplication.setStyle(QStyleFactory.create("Fusion"))

    
    def createRightGroupBox(self):
        
        self.right_gb = QGroupBox("Right")
        # self.right_gb = QLineEdit("Right")
        self.go_button = QPushButton("Run model")
        self.go_button.clicked.connect(self.get_config)

        layout = QVBoxLayout()
        layout.addWidget(self.go_button)
        self.right_gb.setLayout(layout)


    def createLeftGroupBox(self):
        self.input_video_label = QLabel("Input Video")
        self.input_video_box = QLineEdit("C:/Users/RW154JK/OneDrive - EY/Desktop/v1/videos/mini.mp4")
        self.choose_input_video_button = ChooseFileButton(self.input_video_box, "file")

        self.output_folder_label = QLabel("Output folder")
        self.output_folder_box = QLineEdit("C:/Users/RW154JK/OneDrive - EY/Desktop/v1/gui_output")
        self.choose_output_folder_button = ChooseFileButton(self.output_folder_box, "folder")

        self.model_label = QLabel("Model")
        self.model_box = QLineEdit("yolov5s")
        self.choose_model_button = ChooseFileButton(self.model_box, "file")

        self.left_gb = QGroupBox("Left")
        layout = QVBoxLayout()


        layout.addWidget(self.input_video_label)
        layout.addWidget(self.input_video_box)
        layout.addWidget(self.choose_input_video_button)
        layout.addWidget(self.output_folder_label)
        layout.addWidget(self.output_folder_box)
        layout.addWidget(self.choose_output_folder_button)
        layout.addWidget(self.model_label)
        layout.addWidget(self.model_box)
        layout.addWidget(self.choose_model_button)

        self.left_gb.setLayout(layout)

    
    def get_config(self):
        print("Config me baby")
        self.config = {'input_video': self.input_video_box.text(),
                    'output_folder': self.output_folder_box.text(),
                    'model': self.model_box.text()}
        try:
            main(self.config)
        except Exception as e:
            print(str(e))
        self.parent.gotoImageViewer(self.config['output_folder'])
        
    
    

class ChooseFileButton(QPushButton):
    def __init__(self, textbox, mode="file"):
        super(ChooseFileButton, self).__init__(f"Choose {mode}")
        self.mode = mode
        self.clicked.connect(self.choose_file)
        self.textbox = textbox
    
    def choose_file(self):
        if self.mode == "folder":
            output = QFileDialog.getExistingDirectory(self, "Choose file", os.getcwd())
        else:
            output = QFileDialog.getOpenFileName(self, "Choose file", os.getcwd())[0]
        print(output, bool(output))
        if output:
            self.textbox.setText(output)
        return bool(output)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


