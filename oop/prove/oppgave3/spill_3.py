import pygame
from typing import List
import random

FPS = 60
WIDTH, HEIGHT = 400, 600

# Lager eget event slik at vi kan bruke set_timer - https://stackoverflow.com/questions/18948981/do-something-every-x-milliseconds-in-pygame
TIDEVENT, t = pygame.USEREVENT + 1, 10000
FLYTTEVENT, f = pygame.USEREVENT + 2, 2000

FARGER = [(0, 0, 0), (70, 70, 70), (50, 105, 50), (100, 230, 100)]


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.is_running = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.init_consts()
        self.init_timers()

    def init_consts(self) -> None:
        self.farge = FARGER[0]
        self.clicks = 0
        self.click_record = 0
        self.countdown = 10

    def init_timers(self) -> None:
        pygame.time.set_timer(TIDEVENT, t)
        pygame.time.set_timer(FLYTTEVENT, f)

    def draw(self) -> None:
        self.screen.fill(self.farge)
        self.rektangel.draw(self.screen)

        self.draw_text()

        pygame.display.update()

    def draw_text(self) -> None:
        font = pygame.font.SysFont("Arial", 36)
        txtsurf = font.render(f"{self.clicks}", True, (255, 255, 255))
        txtsurf2 = font.render(f"{self.countdown:0.1f}", True, (255, 255, 255))

        self.screen.blit(
            txtsurf,
            (
                self.screen.get_width() // 2 - txtsurf.get_width() / 2,
                txtsurf.get_height() // 2,
            ),
        )

        self.screen.blit(
            txtsurf2,
            (
                self.screen.get_width() // 2 - txtsurf2.get_width() / 2,
                txtsurf2.get_height() // 2 + txtsurf.get_height(),
            ),
        )

    def run(self) -> None:
        self.rektangel = Rektangel()
        while self.is_running:
            self.draw()
            self.handle_events()
            self.countdown -= 1 / FPS
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
                event.type == pygame.MOUSEBUTTONDOWN
                and self.rektangel.rect.collidepoint(pygame.mouse.get_pos())
            ):
                self.clicks += 1

            if event.type == TIDEVENT:
                print(f"Du klarte totalt {self.clicks} klikk på 10 sekund")
                if self.clicks > self.click_record:
                    print(f"Du har fått nå rekord på {self.clicks} klikk")
                    self.click_record = self.clicks

                self.clicks = 0
                self.countdown = 10

                self.bytt_farge()

            if event.type == FLYTTEVENT:
                self.rektangel.flytt()

    def bytt_farge(self) -> None:
        # Liker egentlig ikke å putte en loop her men fant ikke en enkel løsning for å passe på at forrige farge ikke er lik den nye.
        while True:
            valg = random.choice(FARGER)

            if valg == self.farge:
                continue
            else:
                self.farge = valg
                self.screen.fill(valg)
                break


class Rektangel:
    def __init__(self) -> None:
        self.rect = pygame.Rect(WIDTH / 2, HEIGHT / 2, 50, 50)

    def draw(self, screen: pygame.SurfaceType) -> None:
        pygame.draw.rect(screen, (100, 100, 100), self.rect)

    def flytt(self) -> None:
        # Regner - 50 på x og y slik at rektangelet ikke går utenfor skjermen.
        x = random.randint(0, WIDTH - 50)
        y = random.randint(0, HEIGHT - 50)

        self.rect.update(x, y, 50, 50)


if __name__ == "__main__":
    Game().run()
