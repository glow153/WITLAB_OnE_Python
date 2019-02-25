from abc import *


class AbsJTab:
    def __init__(self, title):
        self.leftLayout = None
        self.rightLayout = None
        self.title = title

    @abstractmethod
    def getTitle(self):
        return self.title
