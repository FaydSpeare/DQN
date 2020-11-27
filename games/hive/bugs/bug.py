from games.hive.bugs.direction import Direction

BOTTOM = 0
TOP = 1

class Bug:

    def __init__(self):

        # Neighbours above and below the current bug
        self.v_neighbours = [None, None]

        # Neighbours adjacent to this bugs hexagon
        self.h_neighbours = [None, None, None, None, None, None]


    def is_under_bug(self):
        return self.v_neighbours[TOP] is not None


    def can_slide_to(self, direction):

        if not self.is_occupied(direction):

            left = (direction - 1) % len(Direction)
            right = (direction + 1) % len(Direction)

            # Return True if exactly one is occupied
            return (self.is_occupied(left) + self.is_occupied(right)) == 1

        return False


    def is_occupied(self, direction):
        return self.v_neighbours[direction] is not None


    def get_bug(self, direction):
        return self.v_neighbours[direction]

    def can_move(self):
        return not self.is_under_bug()

