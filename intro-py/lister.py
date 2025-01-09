import random

list = [x**3 for x in range(100)]
list2 = [x**2 for x in range(100)]

# print(list, list2)


rand_list = [random.randint(0, 10) for x in range(96)]


for i in range(4):
    rand_list.append(int(input("Lengde på larve: ")))

print(rand_list)

vær_liste = []

for i in range(7):
    vær_liste.append(
        {
            "dag": i + 1,
            "temperatur": random.randint(5, 15),
            "nedbør": random.randint(0, 50),
            "vindstyrke": random.randint(1, 5),
        }
    )


print(sum(dag["temperatur"] / len(vær_liste) for dag in vær_liste))
