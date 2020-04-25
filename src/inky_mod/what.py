from . import inky


class InkyWHAT(inky.Inky):
    WIDTH = 400
    HEIGHT = 300

    WHITE = 0
    BLACK = 1
    RED = 2
    YELLOW = 2

    def __init__(self, colour):
        inky.Inky.__init__(
            self,
            resolution=(self.WIDTH, self.HEIGHT),
            colour=colour,
            h_flip=False,
            v_flip=False)
