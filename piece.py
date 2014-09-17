__author__ = 'Kokouvi Djogbessi'

class Piece:
    """Contains information about a checkers piece. A piece is a pawn at creation,
    use make_king() to elevate."""

    def __init__(self, is_white, pos):
        """Instantiates a piece object with given properties"""

        self.is_king = False
        self.is_white = is_white
        self.pos = pos

    def make_king(self):
        """Sets this piece as king"""

        self.is_king = True

    def _get_pos(self):
        return self.pos

    def _set_pos(self, pos):
        self.pos = pos

    def _set_is_white(self, is_white):
        print("You can't change the color of a piece!")

    def __repr__(self):
        """Displays the position and type of the piece"""
        if self.is_white:
            color = "White"
        else:
            color = "Black"
        return "{} at {}".format(color, self.pos)
