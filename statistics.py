from PyQt5.QtWidgets import QFileDialog, QMessageBox
from singleton import Singleton
import matplotlib.pyplot as plt
import numpy as np
import datetime
import csv


class Statistics(metaclass=Singleton):
    """ Class that performs calculations and provides statistical data visualisation. """

    def __init__(self):
        self.k_occurrence = np.zeros(16)  # List initialised with 0 that will count the number of tests of given k.
        self.k_accuracy = np.zeros(16)  # List initialised with 0 that will store the accuracy of given k.

    def generate_plots(self, occurrence=None, accuracy=None):
        """ Generate and display the plots for the current tests (if the method is called without parameters) or for
            data loaded from a given file (if the method is called with parameters)
        """

        if not isinstance(occurrence, list):
            occurrence = self.k_occurrence[0:]
            accuracy = self.k_accuracy[0:]

        temp_accuracy = []

        temp_accuracy.extend(accuracy)  # Store the accuracy in a temporal vector so it won't be divided each time.

        for k in range(16):  # Calculate the accuracy for each k.
            if occurrence[k] > 0:
                temp_accuracy[k] /= occurrence[k]

        plt.gca().clear()  # Clear the plot area.
        plt.scatter(range(16), temp_accuracy, label='current accuracy', color='g')

        plt.xlabel('k')
        plt.ylabel('accuracy and occurance')
        plt.title("Accuracy rate plot")

        plt.axis([1, 16, 0.0, 1.0])
        ax = plt.gca()
        ax.set_xticks(np.arange(1, 16, 1))

        plt.legend()
        plt.grid()
        plt.show()

    def load_plot_from_file(self):
        """ Method that parses the data from a file and generates calls generate_plots to display the plots. """

        try:
            file_path = QFileDialog.getOpenFileName(None, 'OpenFile', '.', 'CSV files (*.csv)')

            k_occurrence = [0 for k in range(16)]
            k_accuracy = [0 for k in range(16)]

            with open(file_path[0], "r") as csv_file:
                try:
                    lines = csv.reader(csv_file, delimiter=',')

                    for row in lines:  # Read the file line by line.
                        # The lines are structured as follows:
                        # k, number of tests ran of k, accuracy of tests ran with k
                        k = int(row[0])
                        occurrence = int(row[1])
                        accuracy = float(row[2])

                        k_occurrence[k] = occurrence
                        k_accuracy[k] = accuracy

                        self.generate_plots(k_occurrence, k_accuracy)

                except IOError as e:
                    QMessageBox.warning(None, "Loading data error",
                                        f"There has been an error reading the data from the given file.\n{e}")

        except:
            # Usually bad practice, but an error will be raised when the user quits the open file dialog, so it has to
            # be passed, as it doesn't affect the functionality of the program, nor should it be considered an error
            # in this context
            pass

    def save_in_file(self):
        """ Save the data corresponding to the current tests in a .csv file.
            The format of a line in the file will be as follows:
            k, number of tests ran with k, accuracy of tests ran with k
        """

        try:
            file_path = QFileDialog.getSaveFileName(None, 'SaveFile', f'accuracy-{datetime.datetime.now()}.csv',
                                                    'CSV files (*.csv)')

            with open(file_path[0], "w") as csv_file:
                try:
                    for k in range(1, 16, 1):
                        csv_file.write(f"{k},{int(self.k_occurrence[k])},{self.k_accuracy[k]}\n")

                except IOError as e:
                    QMessageBox.warning(None, "Saving file error",
                                        f"There has been an error trying to save the file.\n{str(e)}")

        except:
            # Usually bad practice, but an error will be raised when the user quits the open file dialog, so it has to
            # be passed, as it doesn't affect the functionality of the program, nor should it be considered an error
            # in this context
            pass
