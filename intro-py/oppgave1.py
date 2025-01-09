import math

r = 31.83
l = 100

def omkrets():
    omkrets = l*2

    omkrets += 2 * r * math.pi

    return omkrets

print(omkrets(), 50 / 3.6, round((omkrets() * 10) / (50 /3.6) / 60, 3))


s = "asdsadadxx"

print(f"{s[:3]}...{s[-3:]}")