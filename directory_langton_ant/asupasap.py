import random

directions = [0, 1]
def random_direction():
    # {1: "N", 2: "E", 3: "S", 4: "W"}
    return random.choice(directions)


value = (random_direction())
print(value)
print("I add 1")
print(directions[((value + 1) % 2)])
