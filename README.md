# Handwritting Recognition System

Python built handwritten digits recognition system using the [k-NN algorithm](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm/).

# Prerequisites

In order to run it you'll need:

* [Python 3.6](https://www.python.org/downloads/release/python-363/)
* [python-mnist](https://github.com/sorki/python-mnist/)
* [PyQt5](https://pypi.python.org/pypi/PyQt5/) - with TkInter integration
* [matplotlib](http://matplotlib.org/users/installing.html/)

# Further instructions

Place the ubyte files from MNIST into a directory called MNIST_samples and put in the same directory as the .py files.
Windows users, please make sure that the file names are as follows, without any extension, otherwise it might not work:
* train-labels-idx1-ubyte
* train-images-idx3-ubyte
* t10k-labels-idx1-ubyte
* t10k-images-idx3-ubyte

In order to run it, open the terminal / cmd in the same directory as the .py files and type python kNN.py