from numpy import tile

import operator


class Classifier:
    """ Class used for classifying digits. """
    @staticmethod
    def classify(in_x, data_set, labels, k):
        """ k-NN static classification method.

            Calculates the Euclidean distance between the input vector (in_x) and each line of the training matrix
            (data_set) and sort the distance indices. Afterwards, 'vote' the k-Nearest Neighbours and then reverse
            sort them with respect to their number of 'votes'
        """
        data_set_img_size = data_set.shape[0]   # shape is a tuple with the form (rows, columns), so shape[0] = #rows.
        diff_mat = tile(in_x, (data_set_img_size, 1)) - data_set  # Stores the vector differences.
        diff_mat **= 2
        sq_distances = diff_mat.sum(axis=1)
        distances = sq_distances ** 0.5  # The final Euclidean distances.
        sorted_dist_indices = distances.argsort()  # The indices that would sort distances.
        class_count = {}

        for i in range(k):  # Get the k-Nearest Neighbours and 'vote' them
            vote_i_label = labels[sorted_dist_indices[i]]
            class_count[vote_i_label] = class_count.get(vote_i_label, 0) + 1
        # Reverse sort the labels.
        sorted_class_count = sorted(class_count.items(), key=operator.itemgetter(1), reverse=True)

        return sorted_class_count[0][0]  # Return the label with most votes
