import tensorflow as tf

from games.connect4 import Connect4
from mcts.quct.quct import quct
from mcts.quct.memory import Memory

'''
def create_network():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(1, activation='softsign')
    ])
    model.compile(loss='mse', optimizer='adam')
    model.build((None, 10))
    return 
'''

def create_network():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(filters=10, kernel_size=3, activation='relu'),
        tf.keras.layers.Conv2D(filters=5, kernel_size=3, activation='relu'),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(1, activation='softsign')
    ])
    model.compile(loss='mse', optimizer='adam')
    model.build((None, 6, 7, 4))
    return model


if __name__ == '__main__':

    network = create_network()
    memory = Memory(size=1024)

    for sp in range(20):
        print("Sp:", sp)

        results = [0, 0, 0]

        for episode in range(20):
            print("Ep:", episode)

            game = Connect4()
            step = 0

            while not game.is_terminal():

                use_best = (step > 3)
                action = quct(game, network, memory, n=50, best=use_best)
                game.act(action)
                step += 1

            result = game.result()[0]
            results[result + 1] += 1

            memory.add_pending_memory((game.to_nn_input(), result))
            memory.push_pending_memory(result)

        print(results)
        X, y = memory.sample(size=1024)
        network.fit(X, y, batch_size=32, epochs=10)
        print()

    network.save('models/connect4_quct_avg')




