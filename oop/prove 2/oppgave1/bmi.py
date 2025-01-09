print("BMI-Kalkulator")

while True:
    try:
        høyde_str = input("Skriv inn høyden i cm: ")
        if høyde_str == "":
            break
        høyde = int(høyde_str)
        vekt = int(input("Skriv inn vekten i kg: "))

        bmi = (vekt) / ((høyde) / 100) ** 2
        if bmi < 18.4:
            bmi_str = "Undervektig"
        elif bmi > 18.4 and bmi < 24.9:
            bmi_str = "Normalvektig"
        else:
            bmi_str = "Overvektig"

        print(f"BMI: {bmi:0.1f} {bmi_str}")

    except ValueError:
        print("Du har kun lov til å skrive heltall. Begynn på nytt \n")

print("Takk for nå")

"""
   f)  Programmet er enda ikke helt feilfritt. Dersom du skriver negative tall i inputten som er heltall vil programmet ikke gi en ValueError og dermed vil 
    det prøve å regne bmi med for eksempel en negativ vekt, noe som vil gi helt feil svar. 
"""
