import random

def create_rd(a,b):
    res = []
    for i in range(500):
        res.append(random.randint(a,b))
    return res

