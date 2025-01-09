
def fib(tall: int, fib_cache = {}):
    if fib_cache.get(tall): 
        return fib_cache[tall]

    if tall <= 1:
        return tall

    fib_n = fib(tall-1, fib_cache) + fib(tall-2, fib_cache)

    fib_cache[tall] = fib_n

    return fib_n

print(fib(15))

# fib_tall = 25


# index = 0
# fib1 = 1
# fib2 = 1
# fib_neste = 0

# while index < fib_tall:
#     fib_neste = fib1 + fib2
#     fib1 = fib2
#     fib2 = fib_neste

#     print(fib_neste)

#     index += 1
