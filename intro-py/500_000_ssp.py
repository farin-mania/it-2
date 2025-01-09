import random
import timeit

def ssp():
    antall = {"stein": 0, "saks": 0, "papir": 0}

    for _ in range(500_000):
        resultat = random.choice(["stein", "saks", "papir"])
        antall[resultat] += 1

    return antall

print(ssp())