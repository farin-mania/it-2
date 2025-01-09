import pygame
from typing import List
import random
import os

FPS = 60
WIDTH, HEIGHT = 400, 600

# Lager eget event slik at vi kan bruke set_timer - https://stackoverflow.com/questions/18948981/do-something-every-x-milliseconds-in-pygame
TIDEVENT, t = pygame.USEREVENT + 1, 10000

FARGER = [(0, 0, 0), (70, 70, 70), (50, 105, 50), (100, 230, 100)]


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.is_running = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.clicks = 0
        self.click_record = 0
        pygame.time.set_timer(TIDEVENT, t)
        self.all_sprites = pygame.sprite.Group()
        self.farge = FARGER[0]
        self.screen.fill(self.farge)

    def draw(self) -> None:
        self.all_sprites.update()
        pygame.display.flip()

    def run(self) -> None:
        self.musepeker = Musepeker()
        while self.is_running:
            self.musepeker.draw(self.screen)
            self.draw()
            self.handle_events()
            self.clock.tick(FPS)

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                print(f"Din rekord var {self.click_record} klikk på 10 sekund")

                # https://www.w3schools.com/python/python_file_write.asp

                f = open("./resultat.txt", "w")
                f.write(f"Din rekord var {self.click_record} klikk på 10 sekund")
                break

            if (
                event.type
                == pygame.MOUSEBUTTONDOWN
                # and self.musepeker.rect.collidepoint(pygame.mouse.get_pos())
            ):
                self.clicks += 1

            if event.type == TIDEVENT:
                print(f"Du klarte totalt {self.clicks} klikk på 10 sekund")
                if self.clicks > self.click_record:
                    print(f"Du har fått nå rekord på {self.clicks} klikk")
                    self.click_record = self.clicks

                self.clicks = 0

                # Liker egentlig ikke å putte en loop her men fant ikke en enkel løsning for å passe på at forrige farge ikke er lik den nye.
                while True:
                    valg = random.choice(FARGER)

                    if valg == self.farge:
                        continue
                    else:
                        self.screen.fill(valg)
                        break


class Musepeker:
    def __init__(self) -> None:
        self.rect = pygame.Rect(WIDTH / 2, HEIGHT / 2, 50, 50)

    def draw(self, screen: pygame.SurfaceType) -> None:
        pygame.draw.rect(screen, (100, 100, 100), self.rect)


game = Game()
game.run()
