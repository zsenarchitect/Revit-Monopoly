# this is the curser to nevigate on the view. Pick marker or player to set obj on locations


from ASSET import Asset


class Cursor(Asset):
    _instance = None

    def __new__(cls, *args, **kwargs):
        """if this works well, will need to try it on Board and Dice class."""
        if not isinstance(cls._instance, cls):
            cls._instance = super(Cursor, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    

    def move_forward(self, step = 1):
        """move the curver object forward by step number
        Args:
            step (positive int, optional): step number. Defaults to 1.
        """
        pass

        pass

    def move_backward(self, step = 1):
        """move the curver object backward by step number
        Args:
            step (positive int, optional): step number. Defaults to 1.
            #this will call the move forward with negative step
        """
        pass

        self.move_forward(-abs(step))

    
    
