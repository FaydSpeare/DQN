from games.hive.bugs.bug import Bug
from games.hive.bugs.direction import Direction

class Ant(Bug):

    def moves(self):

        moves = list()

        if not self.can_move():
            return moves

        # TODO implement

        return moves