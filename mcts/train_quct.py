import tensorflow as tf

from mcts.env.tictactoe import TicTacToe
from mcts.quct.quct import quct, Memory

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
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(1, activation='softsign')
    ])
    model.compile(loss='mse', optimizer='adam')
    model.build((None, 3, 3, 4))
    return model


if __name__ == '__main__':

    network = create_network()
    memory = Memory()

    for sp in range(10):
        print("Sp:", sp)

        results = [0, 0, 0]

        for episode in range(2):
            print("Ep:", episode)

            state = TicTacToe()
            step = 0
            #print_state(state)

            while not state.result()[1]:

                use_best = (step > 1)
                state = quct(state, network, memory, n=50, best=use_best).state
                step += 1
                #print_state(state)

            result = state.result()[0]
            results[result + 1] += 1

            memory.add_pending_memory((state.get_nn_input(), result))
            memory.push_pending_memory(result)

        print(results)
        X, y = memory.sample(size=1024)
        network.fit(X, y, batch_size=32, epochs=10)
        print()

    network.save('models/quct_avg')




