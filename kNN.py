from PyQt5.QtWidgets import QApplication
from canvas import Canvas
from train import Train
from gui import GUI

import sys


def main():
    app_widget = QApplication(sys.argv)  # Initialize the application.
    canvas = Canvas()  # Prepare the canvas.

    train = Train(img_size=28)
    train.train()  # Perform the training

    gui = GUI(canvas, train)  # Initialize the GUI.
    gui.show()

    app_widget.exec_()  # Execute the application.


if __name__ == "__main__":
    main()
