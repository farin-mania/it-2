import random

land = [
    {
        "land": "Norge",
        "hovedstad": "oslo",
        "innbyggere": 5_457_000,
        "naboland": ["sverige", "russland", "finland"]
    },
    {
        "land": "Sverige",
        "hovedstad": "Stockholm",
        "innbyggere": 10_490_000,
        "naboland": ["norge", "finland", "danmark"]
    }, 
    {
        "land": "Malaysia",
        "hovedstad": "Kuala Lumpur",
        "innbyggere": 33_940_000,
        "naboland": ["brunei", "indonesia", "thailand"]
    }, 
    {
        "land": "Canada",
        "hovedstad": "Ottawa",
        "innbyggere": 38_930_000,
        "naboland": ["danmark", "usa"]
    }
]


mulige_spørsmål = [
    "Hva er hovedstaden i:",
    "(Separer med comma), Hvilke naboland har:",
    "Hvor mange innbygere er det i:",
]
antall_spørsmål = 3
poeng = 0

def velg_spørsmål():
    # Todo sjekk om allerede laget samme spørsmål

    spørsmål = random.randint(0,2)
    spørsmål_land = random.choice(land)
    
    return (spørsmål, spørsmål_land)

# Tomme arrays hvor vi lagrer det vi fikk feil på
feil = []
riktig = []

for i in range(antall_spørsmål):
    # Velger spørsmål hvor selve indexen til spørsmålet returnes sammen med infoen om landet som spørsmålet er fra
    spørsmål_tuple = velg_spørsmål()
    land_tekst = spørsmål_tuple[1]["land"]
    index = spørsmål_tuple[0]


    # Henter spørsmål fra spørsmål arrayen ved bruk av indexen som ble generert
    spørsmål = mulige_spørsmål[spørsmål_tuple[0]]
    string = f"{spørsmål} {land_tekst}? "

    try: 
        svar = input(string)

        if index == 0:
            if svar.lower() == spørsmål_tuple[1]["hovedstad"].lower():
                print("riktig")
                riktig.append(i + 1)
                poeng += 1
            else:
                feil.append(i + 1)
                print("feil")

        if index == 1:
            naboland_liste = svar.split(",")
            mulige_naboland= spørsmål_tuple[1]["naboland"]
            antall_naboland = len(spørsmål_tuple[1]["naboland"])
            riktige_naboland = 0

            for gjettet_land in naboland_liste: 
                if gjettet_land.lower() in mulige_naboland:
                    riktige_naboland += 1
        #  print(riktige_naboland)

            if riktige_naboland == antall_naboland:
                poeng +=1
                riktig.append(i + 1)
                print("riktig")
            elif antall_naboland == 3 and riktige_naboland >= 2:
                riktig.append(i + 1)
                poeng +=1
                print("riktig")
            elif antall_naboland >= 4 and riktige_naboland >= 3:
                poeng +=1
                riktig.append(i + 1)
                print("riktig")
            else:
                feil.append(i + 1)
                print("feil")

        if index == 2:
            innbyggere = spørsmål_tuple[1]["innbyggere"]
            range_top = innbyggere* 1.1
            range_bunn = innbyggere * 0.9

            if int(svar) == innbyggere:
                print("Du er jammen god med tall")
                riktig.append(i + 1)
                poeng += 1
            elif (int(svar) > range_bunn and int(svar) < innbyggere) or (int(svar) < range_top and int(svar) > innbyggere):
                print("Du traff +- 10%")
                riktig.append(i + 1)
                poeng += 1
            else:
                feil.append(i + 1)
                print("feil")
    except ValueError:
        print("Du må skrive inn ett tall, begynn på nytt")

        # Stopper tidlig

        # Kilde: https://stackoverflow.com/questions/73663/how-do-i-terminate-a-script#:~:text=A%20simple%20way%20to%20terminate,it%20is%20efficient%20and%20simple.&text=You%20can%20also%20use%20simply%20exit()%20.
        quit()
    

ord = ""

match poeng:
    case 1:
        ord = ("Mindre bra")
    case 2:
        ord = ("Bra")
    case 3: 
        ord = ("Kjempebra")

print(f"Du fikk {poeng} av {antall_spørsmål} riktige svar. Dette er {ord}")

# Kilde: https://stackoverflow.com/questions/22556449/print-a-list-of-space-separated-elements

print("Du svarte feil på spørsmål:", " og ".join(str(x) for x in feil), " og riktig på", " og ".join(str(x) for x in riktig))