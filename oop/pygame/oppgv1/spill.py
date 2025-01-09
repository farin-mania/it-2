import pygame
from typing import List

import pygame.locals

FPS = 60

WIDTH, HEIGHT = 400, 600


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.is_running = True
        self.all_sprites = pygame.sprite.Group()
        self.bullets: List[Bullet] = []

    def run(self) -> None:
        self.kanon = Kanon()
        while self.is_running:
            pressed_down = pygame.key.get_pressed()

            self.handle_events(pygame.event.get())
            self.kanon.handle_pressed_down(pressed_down)
            self.screen.fill((0, 0, 0))
            self.kanon.draw(self.screen)

            for bullet in self.bullets:
                bullet.rect.y -= 2
                if bullet.rect.y < 0:
                    self.bullets.remove(bullet)
                    continue

                bullet.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        if not events:
            return

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print("space")
                bullet = Bullet(self.kanon.rect.x, self.kanon.rect.y - 50)
                self.bullets.append(bullet)

    def handle_pressed_down(self, keys: pygame.key.ScancodeWrapper) -> None:
        pass


class Kanon:
    def __init__(self) -> None:
        self.rect = pygame.Rect(200, 550, 50, 20)

    def draw(self, screen: pygame.SurfaceType) -> None:
        pygame.draw.rect(screen, (100, 100, 100), self.rect)

    def handle_pressed_down(self, keys: pygame.key.ScancodeWrapper) -> None:
        if keys[pygame.K_a]:
            self.rect.x -= 3
        if keys[pygame.K_d]:
            self.rect.x += 3


class Bullet:
    def __init__(self, x: int, y: int) -> None:
        self.rect = pygame.Rect(x, y, 10, 10)

    def draw(self, screen: pygame.SurfaceType) -> None:
        pygame.draw.rect(screen, (0, 0, 255), self.rect)


Game().run()
