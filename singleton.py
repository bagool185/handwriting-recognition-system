class Singleton(type):
    """ Metaclass to implement the Singleton pattern. """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """ Method to verify if there are more than one instance of the same class.
            If the same class is instantiated more than once, that instance will be redirected to the first one.
        """
        if cls not in cls._instances:  # Verify if the class was instantiated.
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]

