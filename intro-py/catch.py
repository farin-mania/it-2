try:
    tall = int(input("Velg et tall: "))

    if tall < 0:
        print("Tall er mindre enn 0")

except ValueError:
    print("Ikke ett tall")
except KeyboardInterrupt:
    print("\n Shutdown")
