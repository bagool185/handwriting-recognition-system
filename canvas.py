from singleton import Singleton
from matplotlib import pyplot as plt
from PyQt5.QtWidgets import QMessageBox
from error_handling import InvalidImageSize
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


class Canvas(metaclass=Singleton):
    """ Class that creates and manipulates canvas. """
    def __init__(self, image=None, img_size=28):
        self.image = image

        try:
            if img_size <= 0:
                raise InvalidImageSize("The image size should be at least 1.")

            self.img_size = img_size

        except InvalidImageSize as e:
            QMessageBox.warning(None, "Invalid image size error message", str(e))

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

    def fill_canvas(self):
        """ Method that draws a digit on the canvas. """
        if self.image is not None:
            # Convert the vectorized image to a matrix.
            new_arr = [[0 for d in range(self.img_size)] for y in range(self.img_size)]
            k = 0

            for i in range(self.img_size):
                for j in range(self.img_size):
                    new_arr[i][j] = self.image[0][k]
                    k += 1  # Change the column in matrix.

            self.figure.clear()

            ax = self.figure.add_subplot(111)  # 111 represents 1x1 grid, first subplot.
            ax.imshow(new_arr, interpolation='nearest')  # Display the image with no interpolation between pixels.

            self.canvas.draw()

    def get_canvas(self):
        """ Canvas getter. """
        self.fill_canvas()

        return self.canvas

    def replace_canvas(self, new_img, new_img_size=28):
        """ Changes the image to be drawn on the canvas and update it. """
        self.image = new_img

        try:
            if new_img_size <= 0:
                raise InvalidImageSize("The image size should be at least 1.")

            self.img_size = new_img_size

        except InvalidImageSize as e:
            QMessageBox.warning(None, "Invalid image size error message", str(e))

        self.fill_canvas()


