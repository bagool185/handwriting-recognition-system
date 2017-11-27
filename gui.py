import sys

from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QMessageBox, QApplication, QSpinBox, QVBoxLayout
from PyQt5.QtCore import QTimer
from error_handling import InvalidK, InvalidN
from statistics import Statistics
from classifier import Classifier
from test import Test


class GUI(QDialog):
    """ Class that creates and manages the main GUI. """

    def __init__(self, canvas, train_object, parent=None):
        super(GUI, self).__init__(parent)

        # General initializations.
        self.statistics = Statistics()
        self.testing_objects = Test()
        self.canvas = canvas

        self.result_label = QLabel()
        self.explanatory_label = QLabel("You can use the spinbox below to change the value of k (1 <= k <= 15)")
        self.test_cases_label = QLabel("Choose the value of n from the spinbox below (1 <= n <= 10000)")
        self.training_mat = train_object.training_mat
        self.training_labels = train_object.training_labels
        self.k = 8
        self.n = 1
        # Widgets initialization.
        self.layout = QVBoxLayout()

        self.k_box = QSpinBox()
        self.n_box = QSpinBox()

        self.n_box.setValue(self.n)
        self.k_box.setValue(self.k)

        self.test_cases_btn = QPushButton("Test n cases")
        self.save_btn = QPushButton("Save current results")
        self.next_img_btn = QPushButton("Get the next image")
        self.graph_btn = QPushButton("See the current accuracy rate plot")
        self.exit_app_btn = QPushButton("Exit application")
        self.graph_from_file_dialog = QPushButton("Generate accuracy rate plot from file")

        self.timer = QTimer()

        self.initialise_event_handling()
        self.prepare_layout()

        self.get_next_image()  # The first image.

        self.setWindowTitle("Handwritting recognition system")

    def prepare_layout(self):
        """ Method that sets GUI's layout and adds to it all the widgets. """
        self.layout.addWidget(self.canvas.get_canvas())
        self.layout.addWidget(self.result_label)
        self.layout.addWidget(self.next_img_btn)
        self.layout.addWidget(self.explanatory_label)
        self.layout.addWidget(self.k_box)

        self.layout.addWidget(self.test_cases_label)
        self.layout.addWidget(self.n_box)
        self.layout.addWidget(self.test_cases_btn)

        self.layout.addWidget(self.graph_btn)
        self.layout.addWidget(self.save_btn)
        self.layout.addWidget(self.graph_from_file_dialog)
        self.layout.addWidget(self.exit_app_btn)

        self.setLayout(self.layout)

    def initialise_event_handling(self):
        """ Connect the widgets events with their corresponding methods. """
        self.k_box.valueChanged.connect(self.change_k)
        self.n_box.valueChanged.connect(self.change_n)

        self.test_cases_btn.clicked.connect(self.classify_n)
        self.next_img_btn.clicked.connect(self.get_next_image)
        self.graph_btn.clicked.connect(self.statistics.generate_plots)
        self.save_btn.clicked.connect(self.statistics.save_in_file)
        self.graph_from_file_dialog.clicked.connect(self.statistics.load_plot_from_file)
        self.exit_app_btn.clicked.connect(GUI.exit_application)

        self.timer.timeout.connect(lambda: self.next_img_btn.setEnabled(True))

    def get_next_image(self):
        """ Method that loads another image from the test set. """
        next_img, next_img_label = self.testing_objects.random_test()

        self.canvas.replace_canvas([next_img])  # Update the canvas with the new digit.
        # Classify the new image.
        classifier_result = Classifier.classify(next_img, self.training_mat, self.training_labels, self.k)

        result = "wrong... :("  # Presume the result was wrong.

        self.statistics.k_occurrance[self.k] += 1  # Increment the number of tests of given k for statistics purposes.

        if classifier_result == next_img_label:  # If the classifier got the digit right.
            result = "right! :)"
            self.statistics.k_accuracy[self.k] += 1  # Increment the number of right classifications.

        self.result_label.setText(f"""
            Expected {next_img_label} and I got {classifier_result}.
            Seems like I was {result}
            k was {self.k}
        """)

        self.next_img_btn.setDisabled(True)  # Disable the button for some time to avoid spam.

        self.timer.start(1000)

    def change_k(self, new_k):
        """ Event handler for the k spinbox. It updates the value of k. """
        try:
            if 1 > new_k or new_k > 15 or int(new_k) != new_k:
                raise InvalidK("Invalid k value. k should be an integer >= 1 and <= 15")

            self.k = new_k

        except InvalidK as e:
            QMessageBox.warning(None, "Invalid k value error message", str(e))
            self.k_box.setValue(self.k)

    def change_n(self, new_n):
        """ Event handler for the n spinbox. It updates the value of n. """
        try:
            if 1 > new_n or new_n > 10000 or int(new_n) != new_n:
                raise InvalidN("Invalid n value. n should be an integer >= 1 and <= 10000")

            self.n = new_n

        except InvalidN as e:
            QMessageBox.warning(None, "Invalid n value error message", str(e))
            self.n_box.setValue(self.n)

    def classify_n(self):
        """ Classify the first n tests from the MNIST test data set, where n is chosen by the user"""
        QMessageBox.information(None, "Notice",
                                "Classification is in progress and might take some  please don't exit the application.")

        errors = 0.0

        for index in range(self.n):
            crt_test = self.testing_objects.testing_images[0]
            crt_label = self.testing_objects.testing_labels[0]

            classifier_result = Classifier.classify(crt_test, self.training_mat, self.training_labels, self.k)

            if classifier_result != crt_label:
                errors += 1

        accuracy = (1.0 - errors / self.n) * 100.0

        classification_results = f"""Classification complete. The results are as follows:
                                     k: {self.k}      number_of_tests: {self.n}
                                     accuracy: {accuracy} %
                                     number_of_errors: {errors}
                                  """

        QMessageBox.information(None, "Classification results", classification_results)

    @staticmethod
    def exit_application():
        if QMessageBox.question(None, '', "Are you sure you want to quit?",
                                QMessageBox.Yes | QMessageBox.No,
                                QMessageBox.No) == QMessageBox.Yes:
            QApplication.quit()
            sys.exit(0)

