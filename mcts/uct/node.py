import numpy as np

C = 2.5

def ucb(c):
    return (c.wins / c.visits) + C * np.sqrt((2.0 * np.log(c.parent.visits)) / c.visits)


class Node:

    def __init__(self, parent, actions):
        self.parent = parent
        self.to_expand = actions
        self.children = dict()
        self.visits = 0
        self.wins = 0

    def expand(self):
        return self.to_expand.pop()

    def is_expanded(self):
        return len(self.to_expand) == 0

    def select_best_child(self):
        action = max(self.children, key=lambda x: ucb(self.children[x]))
        return action, self.children[action]

    def backprop(self, result):
        self.visits += 1
        self.wins += result
        if self.parent is not None: self.parent.backprop(-result)
