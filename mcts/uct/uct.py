import random

from games.base import BaseGame
from mcts.uct.node import Node


def uct(root_game: BaseGame, n=1000, verbose=False, best=False):

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
        result = game.result()[0] if game.is_terminal() else game.simulate()
        result *= -game.to_play()

        # Back-propagate
        node.backprop(result)

    if verbose:
        for action, child in root.children.items():
            print(f'Action: {action} ~ Visits: {child.visits} ~ Value: {child.wins}')
        print()

    if best: return max(root.children, key=lambda a: (root.children[a].visits, root.children[a].wins))

    weights = [c.visits / c.parent.visits for c in root.children.values()]
    return random.choices(list(root.children.keys()), weights=weights, k=1)[0]

