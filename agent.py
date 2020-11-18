import tensorflow as tf
from collections import deque
import random
import numpy as np

class Agent:

    REPLAY_MEMORY_SIZE = 2_500
    BATCH_SIZE = 500
    DISCOUNT = 0.99
    UPDATE_TARGET = 200

    def __init__(self, model_factory):
        self.main_model = model_factory()
        self.target_model = model_factory()
        self.replay_memory = deque(maxlen=Agent.REPLAY_MEMORY_SIZE)
        self.update_target_counter = 0

    @classmethod
    def load_agent(cls, model):
        trained_agent = Agent(lambda : None)
        trained_agent.main_model = model
        trained_agent.target_model = model
        return trained_agent

    def duplicate(self):
        copy_agent = Agent(lambda: None)
        copy_agent.main_model = self.main_model
        copy_agent.target_model = self.target_model
        return copy_agent


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


    def get_best_action(self, action_state_pairs, inverted=False, verbose=False):
        states = np.array([s for _, s in action_state_pairs]).astype(np.float64)
        q_values = self.main_model.predict(states)
        if verbose:
            print({action_state_pairs[i][0]: float(q) for i, q in enumerate(q_values)})
        best_action_idx = np.argmax(q_values) if not inverted else np.argmin(q_values)
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