
x = [0 for _ in range(42)]
wins = []

# horizontal
for row in range(6):
    for col in range(7):
        if col <= 3:
            i = 7 * row + col
            wins.append([i, i+1, i+2, i+3])

print(len(wins))

# vertical
for col in range(7):
    for row in range(6):
        if row <= 2:
            i = 7 * row + col
            wins.append([i, i+7, i+14, i+21])
print(len(wins))

# diagonal up right
for row in range(6):
    if row <= 2:
        for col in range(7):
            if col <= 3:
                i = 7 * row + col
                wins.append([i, i + 8, i + 16, i + 24])
print(len(wins))

# diagonal up left
for row in range(6):
    if row <= 2:
        for col in range(7):
            if col >= 3:
                i = 7 * row + col
                wins.append([i, i + 6, i + 12, i + 18])
print(len(wins))

print(wins)
print(len(wins))
