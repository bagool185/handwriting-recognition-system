from PyQt5.QtWidgets import QFileDialog, QMessageBox
from singleton import Singleton
import matplotlib.pyplot as plt
import numpy as np
import datetime
import csv
import os


class Statistics(metaclass=Singleton):
    """ Class that performs calculations and provides statistical data visualisation. """

    def __init__(self):
        self.k_occurrance = np.zeros(16)  # List initialised with 0 that will count the number of tests of given k.
        self.k_accuracy = np.zeros(16)  # List initialised with 0 that will store the accuracy of given k.

    def generate_plots(self, occurrance=None, accuracy=None):
        """ Generate and display the plots for the current tests (if the method is called without parameters) or for
            data loaded from a given file (if the method is called with parameters)
        """

        if not isinstance(occurrance, list):
            occurrance = self.k_occurrance
            accuracy = self.k_accuracy

        for k in range(1, 16, 1):  # Calculate the accuracy for each k.
            if occurrance[k] > 0:
                accuracy[k] /= occurrance[k]

        plt.gca().clear()  # Clear the plot area.
        plt.scatter(range(1, 17, 1), accuracy, label='current accuracy', color='g')
        plt.plot(range(1, 17, 1), occurrance, label='occurrance', color='r')

        plt.xlabel('k')
        plt.ylabel('current accuracy')
        plt.title("Accuracy rate plot")

        ax = plt.gca()
        ax.set_xticks(np.arange(1, 16, 1))

        plt.legend()
        plt.grid()
        plt.show()

    def load_plot_from_file(self):
        """ Method that parses the data from a file and generates calls generate_plots to display the plots. """

        try:
            file_path = QFileDialog.getOpenFileName(None, 'OpenFile', '.', 'CSV files (*.csv)')

            if os.path.exists(file_path):

                k_occurrance = [0 for k in range(1, 17, 1)]
                k_accuracy = [0 for k in range(1, 17, 1)]

                with open(file_path[0], "r") as csv_file:
                    try:
                        lines = csv.reader(csv_file, delimiter=',')

                        for row in lines:  # Read the file line by line.
                            # The lines are structured as follows:
                            # k, number of tests ran of k, accuracy of tests ran with k
                            k = int(row[0])
                            occurrance = int(row[1])
                            accuracy = float(row[2])

                            k_occurrance[k] = occurrance
                            k_accuracy[k] = accuracy
                    except IOError:
                        QMessageBox.warning(None, "Loading data error",
                                            "There has been an error reading the data from the given file")

                self.generate_plots(k_occurrance, k_accuracy)
        except:
            # An error will be raised when the user quits the open file dialog, so it has to be passed.

            pass

    def save_in_file(self):
        """ Save the data corresponding to the current tests in a .csv file.
            The format of a line in the file will be as follows:
            k, number of tests ran with k, accuracy of tests ran with k
        """

        try:
            file_path = QFileDialog.getSaveFileName(None, 'SaveFile', f'accuracy-{datetime.datetime.now()}.csv',
                                                    'CSV files (*.csv)')

            if os.path.exists(file_path):
                with open(file_path[0], "w") as csv_file:
                    try:
                        for k in range(1, 16, 1):
                            csv_file.write(f"{k},{self.k_occurrance[k]},{self.k_accuracy[k]}\n")

                    except IOError:
                        QMessageBox.warning(None, "Saving file error",
                                            "There has been an error trying to save the file. Please try again.")

        except:
            # An error will be raised when the user quits the save file dialog, so it has to be passed.
            pass
