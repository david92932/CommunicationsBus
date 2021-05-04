class TimelineConfiguration():
    """
    Configuration parameter for timeline boxes
    """

    def __init__(self):

        # the number of pixels to represent 1 ms of time
        # EX: 10ms command = 40pxs of horizontal space
        # when pixelsPersMillisecond = 4
        self.pixelsPerMillisecond = 4

        # number of pixels of empty space between each timeline row
        self.rowSpacing = 25

        # number of pixels for the height of each box
        self.boxHeight = 50