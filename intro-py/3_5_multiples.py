total_sum = 0

for i in range(0, 1000):
    print(i)
    if i % 3 == 0 or i % 5 == 0:
        total_sum += i

print(total_sum)