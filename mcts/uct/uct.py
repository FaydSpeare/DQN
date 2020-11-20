import numpy as np
import random

def uct(state, n=1000, verbose=False, best=False):
    print(state.turn)
    root = Node(parent=None, state=state)

    for sim in range(n):

        # Selection (Select a node to expand)
        node = root
        while node.is_expanded() and not node.is_terminal():
            node = node.get_best_child()

        # Expansion (Add new child to selected node)
        child_node = node.expand() if not node.is_terminal() else node

        # Rollout (simulate game from child node)
        result = child_node.rollout()
        result *= -child_node.state.turn

        # Back-propagate
        child_node.backprop(result)

    if verbose:
        for c in root.children:
            print(c.state.state, c.visits, c.wins)

    if best: return max(root.children, key=lambda c: (c.visits, c.wins))

    weights = [c.visits / c.parent.visits for c in root.children]
    return random.choices(root.children, weights=weights, k=1)[0]



class Node:

    C = 2.5

    def __init__(self, parent, state):
        self.parent = parent
        self.state = state
        self.child_states = state.get_next_states()
        self.children = list()
        self.visits = 0
        self.wins = 0

    def expand(self):
        child = Node(parent=self, state=self.child_states.pop())
        self.children.append(child)
        return child

    def is_expanded(self):
        return len(self.child_states) == 0

    def get_best_child(self):
        return max(self.children, key=lambda c: (c.wins / c.visits) +
            Node.C * np.sqrt((2.0 * np.log(self.visits)) / c.visits))

    def rollout(self):
        return self.state.simulate()

    def backprop(self, result):
        self.visits += 1
        self.wins += result
        if self.parent is not None: self.parent.backprop(-result)

    def is_terminal(self):
        return self.state.result()[1]
