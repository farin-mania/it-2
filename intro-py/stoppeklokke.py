import time

i = 0
sekund = 0
ms = 0
minutt = 0

while True:
    if sekund % 60 == 0 and sekund != 0:
        sekund = 0
        minutt +=1
    if ms == 10:
        ms = 0
    if i % 10 == 0 and i != 0:
        sekund += 1

    print(minutt, sekund, ms)

    time.sleep(0.10)
    ms += 1
    i += 1