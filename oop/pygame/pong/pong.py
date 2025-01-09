import pygame


def run():
    clock = pygame.time.Clock()
    pygame.init()

    # Set opp skjermen
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pong")

    # Set opp fargane
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    poeng_1 = 0
    poeng_2 = 0

    # Set opp paddlane og ballen
    paddle1 = pygame.Rect(50, 250, 20, 100)
    paddle2 = pygame.Rect(730, 250, 20, 100)
    ball = pygame.Rect(390, 290, 20, 20)

    running = True

    ball_x_velocity = 6
    ball_y_velocity = 6

    while running:
        # Handter hendingar
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and paddle2.y > 3:
            print("up", paddle2.y)
            paddle2.y -= 6
        if keys[pygame.K_DOWN] and paddle2.y < 510:
            print("down", paddle2.y)
            paddle2.y += 6

        if keys[pygame.K_w] and paddle1.y > 3:
            paddle1.y -= 6
        if keys[pygame.K_s] and paddle1.y < 510:
            paddle1.y += 6

        # Oppdater spelets tilstand

        if ball.colliderect(paddle1) or ball.colliderect(paddle2):
            ball_x_velocity = ball_x_velocity * -1

        if ball.x > 790:
            poeng_1 += 1
            reset_ball(ball)

        if ball.x < 5:
            poeng_2 += 1
            reset_ball(ball)

        if ball.y > 590 or ball.y < 10:
            ball_y_velocity = ball_y_velocity * -1

        ball.x += ball_x_velocity
        ball.y += ball_y_velocity

        # Teikn alt
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, paddle1)
        pygame.draw.rect(screen, WHITE, paddle2)
        pygame.draw.ellipse(screen, WHITE, ball)

        font = pygame.font.SysFont("Arial", 36)
        txtsurf = font.render(f"{poeng_1} : {poeng_2}", True, WHITE)

        screen.blit(txtsurf, (screen.get_width() // 2 - 30, txtsurf.get_height() // 2))

        # Oppdater skjermen
        pygame.display.flip()

        # Avgrens bildefrekvensen
        clock.tick(60)


def reset_ball(ball: pygame.Rect):
    ball.x = 390
    ball.y = 390


run()
