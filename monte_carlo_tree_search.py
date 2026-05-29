import random

class Node:

    def __init__(self, state):
        self.state = state
        self.wins = 0
        self.visits = 0

def simulate():

    return random.choice([0,1])

root = Node("Start")

for i in range(1000):

    result = simulate()

    root.visits += 1
    root.wins += result

print("Visits =", root.visits)
print("Wins =", root.wins)
print("Win Rate =", root.wins/root.visits)
