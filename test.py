from singleton import Singleton
from mnist import MNIST
import random


class Test(metaclass=Singleton):
    """ Class that manipulates the test data set from the MNIST data set. """
    def __init__(self):
        mndata = MNIST('MNIST_samples')  # Load the MNIST data set
        self.testing_images, self.testing_labels = mndata.load_testing()  # Load the MNIST test data set.
        self.test_size = len(self.testing_images)
        self.chosen_test_indexes = list()  # Store the random chosen indexes so tests won't repeat.

    def random_test(self):
        """ Get a random test image and its corresponding label. """
        random_index = random.randrange(self.test_size)
        # Choose a random index that hasn't been used before.
        while random_index in self.chosen_test_indexes:
            random_index = random.randrange(self.test_size)

        self.chosen_test_indexes.append(random_index)
        # Return a tuple consisting of the image and its corresponding label.
        return self.testing_images[random_index], self.testing_labels[random_index]
