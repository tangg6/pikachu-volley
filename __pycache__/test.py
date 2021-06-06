import pygame
pygame.init()

window_w = 800
window_h = 600

white = (255, 255, 255)
black = (0, 0, 0)

FPS = 60

window = pygame.display.set_mode((window_w, window_h))
pygame.display.set_caption("Game: ")
clock = pygame.time.Clock()


def game_loop():
    block_size = 20
    x = 5
    y = 0
    grav = 0.5
    friction_x = 1
    pos_x = 40
    pos_y = 40

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pos_x += x
        pos_y += y

        if pos_y + block_size > window_h and y <= 2.0:
            x = 0
            y = 0
            grav = 0
            friction_x = 0
        if pos_y + block_size > window_h or pos_y < 20:
            y = -y
            print(pos_y)
        if pos_x + block_size > window_w or pos_x < 20:
            x = -(x*friction_x)

        # DRAW
        window.fill(white)
        pygame.draw.circle(window, black,(pos_x, pos_y,), block_size)
        pygame.display.update()
        clock.tick(FPS)
        y += grav


game_loop()