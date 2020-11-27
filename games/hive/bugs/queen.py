from games.hive.bugs.bug import Bug
from games.hive.bugs.direction import Direction

class Queen(Bug):

    def moves(self):

        moves = list()

        if not self.can_move():
            return moves

        for d in Direction:

            # Sliding moves
            if self.can_slide_to(d):
                moves.append(f'Slide {d}')

        return moves