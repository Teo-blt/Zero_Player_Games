import random
import threading
import time

directions = [0, 1]
def random_direction():
    # {1: "N", 2: "E", 3: "S", 4: "W"}
    return random.choice(directions)


value = (random_direction())
print(value)
print("I add 1")
print(directions[((value + 1) % 2)])


def function_test():
    p = 0
    for i in range(0, 100):
        p += i
    return p


def auto():
    start_time = time.time()
    function_test()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Function execution time: {execution_time:.6f} seconds")
    threading.Timer(0.5, auto).start()

auto()
