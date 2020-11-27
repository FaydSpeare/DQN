from games.hive.bugs.bug import Bug
from games.hive.bugs.direction import Direction

class Grasshopper(Bug):

    def moves(self):

        moves = list()

        if not self.can_move():
            return moves

        for d in Direction:

            if not self.is_occupied(d):
                continue

            bug = self
            while bug.is_occupied(d):
                bug = bug.get_bug(d)

            # Add move

        return moves