from typing import List
import random

endinger = ["en", "ene", "ens"]
spesialtegn = ["#", "!", "*", "$", "%", "&"]

problematiske_ord = [
    {
        "ord": "fis",
        "unntak": ["ski"],
       "erstatning": "promp"
    },
    {   
        "ord": "fuck",
        "unntak": []
    }, 
    {
        "ord": "idiot",
        "unntak": []
    }, 
    {
        "ord": "helvete",
        "unntak": []
    },
    {
        "ord": "taper",
        "erstatning": "smarting",
        "unntak": []
    }
]

def sensurer(setning: str) -> str: 
    for ord in setning.split(" "):
        # Liker egentlig ikke å loope to ganger, men gjør ingen forskjell fordi vi da ikke bryker in, som vil gi oss samme time complexity
        for problematisk_ord in problematiske_ord:
            # Sjekker om ordet er nøyaktig det vi skal sensurere
            if ord.lower() == problematisk_ord["ord"] and not er_unntakk(setning, ord, problematisk_ord["unntak"]):
                setning = erstatt_ord(problematisk_ord, setning, ord)
            for ending in endinger:
                # Sjekker om ordet har en ending
                if ord.lower().replace(ending, "") == problematisk_ord["ord"].lower():
                    setning = erstatt_ord(problematisk_ord, setning, ord)

                # Sjekker om noen prøver å lure seg forbi
                for tegn in spesialtegn: 
                    if ord.lower().replace(ending, "").replace(tegn, "") == problematisk_ord["ord"] and not er_unntakk(setning, ord, problematisk_ord["unntak"]):
                        setning = erstatt_ord(problematisk_ord, setning, ord)



    print(setning)
    return setning

def er_unntakk(setning: str, ord: str, unntak_list: List) -> bool:
    for unntak in unntak_list:
        if unntak in setning.lower():
            return True
    return False 


def gjør_uleselig(ord: str) -> str:
    nytt_ord = ""
    ord_lengde = len(ord)
    for _ in range(ord_lengde):
        nytt_ord += random.choice(["#", "$", "&", "@", "!"])

    return nytt_ord

def erstatt_ord(problematisk_ord, setning, ord) -> str:
    if "erstatning" in problematisk_ord:
        setning = setning.replace(ord.lower(), problematisk_ord["erstatning"])
    else:
         setning = setning.replace(ord.lower(), gjør_uleselig(ord))
    return setning



sensurer("Den som fi#sen først er var, den er fisens rette far")
sensurer("FIS globally governs skiing and snowboarding and oversees over 7000 events annually in Alpine, Cross-Country, Ski Jumping, Nordic Combined and many more.")