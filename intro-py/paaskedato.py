def dato(årstall: int):
    a = årstall % 19
    b = årstall // 100
    c = årstall % 100
    print("asd")
    d = b // 4
    e = b % 4
    
    f = (b + 8) // 25
    g = (b - f + 1) // 3

    h = (19 * a + b - d - g + 15) % 30
    
    i = c // 4
    k = c % 4

    l = (32 + 2 * e + 2 * i - h - k) % 7

    m = (a + 11 * h + 22 * l) // 451
    n = (h + l - 7 * m + 114) // 31
    p = (h + l - 7 * m + 114) % 31

    print(f"Påskedag: {p + 1}. {n}. måned")

# Test for de siste 6 årene
for år in range(2019, 2030):
    print(f"\nÅr {år}:")
    dato(år)
