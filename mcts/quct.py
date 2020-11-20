import numpy as np
from collections import deque
import random

def quct(state, network, memory, n=10, best=False, verbose=False):

    root = Node(parent=None, state=state)

    for sim in range(n):

        # Selection (Select a node to expand)
        node = root
        while node.is_expanded() and not node.is_terminal():
            node = node.get_best_child()

        # Expansion (Add new child to selected node)
        child_node = node.expand() if not node.is_terminal() else node

        # Rollout (simulate game from child node)
        if child_node.is_terminal():
            result = child_node.state.result()[0]
        else:
            result = network.predict([child_node.state.get_nn_input()])[0][0]

        #result *= state.turn
        result *= -child_node.state.turn

        # Back-propagate
        child_node.backprop(result)

    # Add memory for training
    s = state.get_nn_input()
    q = root.wins / root.visits

    if memory is not None:
        memory.add_pending_memory((s, q))

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


class Memory:

    def __init__(self, size=1024):
        self.memory = deque(maxlen=size)
        self.pending_memory = []

    def add_pending_memory(self, memory):
        self.pending_memory.append(memory)

    def push_pending_memory(self, result):
        for memory in self.pending_memory:
            self.memory.append((*memory, result))
        self.pending_memory = []

    def sample(self, size=128):
        sample = random.sample(self.memory, k=min(size, len(self.memory)))
        X, y = [], []
        for s, q, z in sample:
            X.append(s)
            y.append((z + q) / 2)
        return np.array(X), np.array(y)