from PyQt5.QtWidgets import QMessageBox
from singleton import Singleton
from mnist import MNIST
from numpy import *

import os

class Train(metaclass=Singleton):
    """ Class that manipulates the training data set from the MNIST data set. """
    def __init__(self, img_size=28):
        mndata = MNIST(os.path.join(os.getcwd(),'MNIST_samples'))  # Load the MNIST data set.
        self.training_images, self.training_labels = mndata.load_training()  # Load the training data set.
        self.train_size = len(self.training_images)
        self.img_size = img_size
        self.training_mat = zeros((self.train_size, img_size * img_size))  # Fill the matrix with zeros.

    def train(self):
        """ Method that carries the training. """

        QMessageBox.information(None, "Training in progress", "Training in progress. Please, press OK and wait.")

        # Build a training matrix with each line being a vector representing an image.
        for i in range(self.train_size):
            self.training_mat[i, :] = self.training_images[i]

        QMessageBox.information(None, "Training complete!",
                                "Training completed successfully! Thank you for your patience! Press ok to begin.")
