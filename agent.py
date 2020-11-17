import tensorflow as tf
from collections import deque
import random
import numpy as np

class Agent:

    REPLAY_MEMORY_SIZE = 1000
    BATCH_SIZE = 100
    DISCOUNT = 0.95
    UPDATE_TARGET = 50

    def __init__(self, model_factory):
        self.main_model = model_factory()
        self.target_model = model_factory()
        self.replay_memory = deque(maxlen=Agent.REPLAY_MEMORY_SIZE)
        self.update_target_counter = 0


    def update_replay_memory(self, replay):
        self.replay_memory.append(replay)


    def train(self):

        if len(self.replay_memory) < Agent.BATCH_SIZE:
            return

        batch = random.sample(self.replay_memory, Agent.BATCH_SIZE)

        next_states = np.array([replay[3] for replay in batch])
        next_state_qs = self.target_model.predict(next_states)

        X, y = [], []
        for idx, (state, action, reward, next_state, done) in enumerate(batch):
            new_q_value = reward + Agent.DISCOUNT * next_state_qs[idx] if not done else reward
            X.append(state)
            y.append([new_q_value])

        X = np.array(X, dtype=np.float64)
        y = np.array(y, dtype=np.float64)

        self.main_model.fit(X, y, shuffle=False, batch_size=Agent.BATCH_SIZE, verbose=False)

        self.update_target_counter += 1
        if self.update_target_counter > Agent.UPDATE_TARGET:
            #print('setting target weights')
            self.target_model.set_weights(self.main_model.get_weights())
            self.update_target_counter = 0


    def get_best_action(self, action_state_pairs):
        states = np.array([s for _, s in action_state_pairs]).astype(np.float64)
        q_values = self.main_model.predict(states)
        best_action_idx = np.argmax(q_values)
        return action_state_pairs[best_action_idx][0]





if __name__ == '__main__':

    def __create_model():
        model = tf.keras.models.Sequential(
            tf.keras.layers.Dense(16),
            tf.keras.layers.Dense(1)
        )
        model.compile(loss='mse', optimizer='adam')
        return model

    agent = Agent(__create_model)