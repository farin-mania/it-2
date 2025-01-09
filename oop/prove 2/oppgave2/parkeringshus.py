from typing import List
from enum import Enum
from datetime import datetime


class BilFarge(Enum):
    RØD = "Rød"
    HVIT = "Hvit"
    SVART = "Svart"
    GRÅ = "Grå"


class Bil:
    def __init__(
        self, skilt: str, bilmerke: str, farge: BilFarge, parkeringskostnad: float
    ) -> None:
        self.skilt = skilt
        self.bilmerke = bilmerke
        self.farge = farge
        self.parkeringskostnad = parkeringskostnad

        print(f"Oprettet {farge.value} {bilmerke} med reg.nr. {skilt}")

    def __str__(self) -> str:
        return f"{self.get_skilt()} {self.get_merke()}"

    def get_skilt(self) -> str:
        return self.skilt

    def get_farge(self) -> BilFarge:
        return self.farge

    def get_kostnad(self) -> float:
        return self.parkeringskostnad

    def get_merke(self) -> str:
        return self.bilmerke


class PersonBil(Bil):
    def __init__(self, skilt: str, bilmerke: str, farge: BilFarge) -> None:
        parkeringskostnad = 1.5
        super().__init__(skilt, bilmerke, farge, parkeringskostnad)


class LasteBil(Bil):
    def __init__(self, skilt: str, bilmerke: str, farge: BilFarge) -> None:
        parkeringskostnad = 3
        super().__init__(skilt, bilmerke, farge, parkeringskostnad)


class ParkertBil:
    def __init__(self, tidspunkt: int, bil: Bil) -> None:
        self.tidspunkt = tidspunkt
        self.parkert_bil = bil

    def beregn_kostnad(self, utkjøringstidspunkt: int) -> float:
        # Runder til nermeste minutt
        minutter_parkert = self.beregn_minutter(utkjøringstidspunkt)

        return minutter_parkert * self.parkert_bil.get_kostnad()

    def beregn_minutter(self, tidspunkt: int) -> int:
        return (tidspunkt - self.tidspunkt) // 60


class Parkeringshus:
    def __init__(self, parkeringsplasser: int) -> None:
        self.ledige_parkeringsplasser = parkeringsplasser
        self.parkerte_biler: List[ParkertBil] = []

        print(f"Opprettet parkeringshus med {parkeringsplasser} plasser")

    def innkjøring(self, bil: Bil, tidspunkt: datetime) -> None:
        # https://stackoverflow.com/questions/19801727/convert-datetime-to-unix-timestamp-and-convert-it-back-in-python

        if self.ledige_parkeringsplasser <= 0:
            print(
                "Det er ingen ledige parkeringsplasser. Vent til en annen bil har kjørt ut."
            )
            return

        unix_tidspunkt = tidspunkt.timestamp()
        parkert_bil = ParkertBil(unix_tidspunkt, bil)
        self.parkerte_biler.append(parkert_bil)
        self.ledige_parkeringsplasser -= 1

        print(
            f"{bil.get_skilt()} {bil.get_farge().value} {bil.get_merke()} kjørte inn klokken {tidspunkt.time()}."
        )

        self.print_parkeringsplasser()

    def utkjøring(self, bil: Bil, tidspunkt: datetime) -> None:
        unix_tidspunkt = tidspunkt.timestamp()
        for x in self.parkerte_biler[:]:
            if x.parkert_bil.get_skilt() == bil.get_skilt():
                kostnad = x.beregn_kostnad(unix_tidspunkt)
                minutter = x.beregn_minutter(unix_tidspunkt)
                self.ledige_parkeringsplasser += 1
                self.parkerte_biler.remove(x)
                print(
                    f"{bil.get_skilt()} {bil.get_farge().value} {bil.get_merke()} kjørte ut {tidspunkt.time()}. Bilen var parkert i {minutter:0.0f} minutter og det kostet {kostnad} kr"
                )
                self.print_parkeringsplasser()
                break

    def print_parkeringsplasser(self) -> None:
        print(
            f"Det er {self.ledige_parkeringsplasser} parkeringsplasser igjen",
            end="\n\n",
        )

    def print_biler_av_farge(self, farge: BilFarge):
        lik_farge = []
        for parkertbil in self.parkerte_biler:
            if parkertbil.parkert_bil.get_farge() == farge:
                lik_farge.append(parkertbil.parkert_bil)

        print(
            f"Parkerte biler som er {farge.value}:\n{"\n".join(str(x) for x in lik_farge)} \n"
        )


if __name__ == "__main__":
    parkeringshus = Parkeringshus(20)
    bil = PersonBil("EL51235", "Tesla", BilFarge.GRÅ)
    bil2 = LasteBil("PA1512", "Volvo", BilFarge.GRÅ)

    parkeringshus.innkjøring(bil, datetime(2024, 11, 3, 16, 24, 13))
    parkeringshus.innkjøring(bil2, datetime(2024, 11, 3, 16, 24, 13))
    #  parkeringshus.utkjøring(bil, datetime(2024, 11, 3, 16, 27, 13))

    parkeringshus.print_biler_av_farge(BilFarge.GRÅ)

    parkeringshus.utkjøring(bil2, datetime(2024, 11, 3, 17, 24, 13))

    """
    d)
    Mulig feil som kan oppstå er blant annet at biler kan registrere tiden, og dermed bestemmer hvor mye de betaler selv.
    Samtidig er det mulig at noen registrerer feil tidspunkt, som kan føre til at kostnaden i noen tilfeller kan være negativ.
    Noe lignende kan skje dersom en person registrerer samme skilt to ganger. Da vet programmet ikke hvilken bil som er hvilken,
    som vil føre til at den første bilen som blir funnet når vi itererer over arrayen er den som f.eks. da betaler når vi kjører ut.
    Det kan da hende at den ene bilen betaler for den andre og omvendt.  
    """
