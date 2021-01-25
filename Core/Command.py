from GUI.MyTimelineWidget import MyTimelineWidget

class Command():

    def __init__(self, z, x, c, v, b, n, m, a):

        self.z = z
        self.x = x
        self.c = c
        self.v = v
        self.b = b
        self.n = n
        self.m = m
        self.a = a
        # self.timelineWidget = timeline_widget

    def getCommandPropertyList(self):

        return [self.z, self.x, self.c, self.v, self.b, self.n, self.m, self.a]

    def updateCommand(self, column, new_value):

        print(column)
        print(new_value)

