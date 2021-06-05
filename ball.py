import pygame
import os
import time
os.environ['SDL_VIDEO_WINDOW_POS'] = '200,200'

pygame.init()





class Ball:
    def __init__(self) :
        pass
        

    def draw_ball(surface):
        window_w = 800
        window_h = 600

        white = (255, 255, 255)
        black = (0, 0, 0)

        FPS = 60

        clock = pygame.time.Clock()
        block_size = 20
        x = 5
        y = 0
        grav = 0.5
        friction_x = 1
        pos_x = 40
        pos_y = 40

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
        pygame.draw.circle(surface, black,(pos_x, pos_y,), block_size)
        clock.tick(FPS)
        y += grav
            

    #def hit_ball(player):