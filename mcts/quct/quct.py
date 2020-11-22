import numpy as np
import random

from mcts.uct.node import Node
from games.base import BaseGame


def quct(root_game: BaseGame, network, memory, n=50, verbose=False, best=False):

    root = Node(parent=None, actions=root_game.get_legal_moves())

    for sim in range(n):

        # Clone game
        game = root_game.copy()

        # Selection (Select a node to expand)
        node = root
        while node.is_expanded() and not game.is_terminal():
            action, node = node.select_best_child()
            game.act(action)

        # Expansion (Adding all the children)
        if not game.is_terminal():
            action = node.expand()
            game.act(action)
            child = Node(parent=node, actions=game.get_legal_moves())
            node.children[action] = child
            node = child

        # Rollout (simulate game from child node)
        if game.is_terminal():
            result = game.result()[0]
        else:
            nn_input = np.array([game.to_nn_input()])
            result = network.predict(nn_input).flatten()[0]

        result *= -game.to_play()

        # Back-propagate
        node.backprop(result)

    # Add memory for training
    s = root_game.to_nn_input()
    q = root.wins / root.visits

    if memory is not None:
        memory.add_pending_memory((s, q))

    if verbose:
        for action, child in root.children.items():
            print(f'Action: {action} ~ Visits: {child.visits} ~ Value: {child.wins}')
        print()

    if best: return max(root.children, key=lambda a: (root.children[a].visits, root.children[a].wins))

    weights = [c.visits / c.parent.visits for c in root.children.values()]
    return random.choices(list(root.children.keys()), weights=weights, k=1)[0]


