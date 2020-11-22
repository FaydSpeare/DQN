from collections import deque
import random
import numpy as np

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