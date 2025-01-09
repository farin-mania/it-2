import re

maaneder = "JanFebMarAprMaiJunJulAugSepOktNovDes"
maanederList = re.findall('[A-Z][^A-Z]*', maaneder)

tall = int(input("Måned"))

print(maanederList[tall - 1])

