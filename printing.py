def print_state(s):

    map = {
        0: '-',
        1: 'x',
        2: 'o'
    }

    for i in range(3):
        for j in range(3):
            c = None
            for k in range(3):
                if s[(i * 3 + j) + 9 * k] == 1:
                    c = map[k]
                    break
            print(c, end='')
        print()