import pygame as pg
from os import listdir


class Sang:
    def __init__(self, path: str) -> None:
        self.path = path
        pass

    def __str__(self) -> str:
        return f"{self.path}"


class Musikkspiller:
    def __init__(self) -> None:
        pass

    def run(self):
        sang_list: list[Sang] = []

        sanger = listdir("./musikk")
        for sang in sanger:
            if not sang.endswith(".mp3"):
                continue

            sang_list.append(Sang(f"./musikk/{sang}"))

        print(sang_list[0])


Musikkspiller().run()
