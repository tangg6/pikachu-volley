import pygame
import pygame_menu
from pygame.locals import *
from ball import Ball

pygame.init()

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '1000,200'

import threading

def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True # Use deamon thread
    thread.start()

#------------------------ Open server ------------------------------

import socket
HOST = '127.0.0.1'
PORT = 62107
connection_established = False

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((HOST,PORT)) # เชื่อมต่อ

#------------------------- Recieve data from client --------------------------------

def recieve_data():
    global x1,y1
    while True:
        data = server.recv(1024).decode()
        data = data.split('-')
        #print(data)
        x1, y1 = float(data[0]), float(data[1])

create_thread(recieve_data)

#------------------------- Create a display of game ---------------------------------
size_game = (800,600)
surface = pygame.display.set_mode(size_game)
pygame.display.set_caption("Ball") #caption
# icon = pygame.image.load(os.path.join('games.png'))
# pygame.display.set_icon (icon)
clock = pygame.time.Clock() 
y = surface.get_height()-70

ball = Ball()

x1, y1 = 375, 490

def start_the_game():
    # Main game

    running = True
    x2, y2 = 675, 500

    move = 20
    jump = False
    jump_count = 10
    grav = 0.6

    surface = pygame.display.set_mode(size_game)
    bg = pygame.image.load("pikachu_background.png")
    
    while running:
        
        surface.blit(bg, (0, 0))
        print("check")
        
        keyspressed = pygame.key.get_pressed()
        for event in pygame.event.get(): # User did something
            #print(event)    # Useful debugging tip    
            if event.type == pygame.QUIT: # If user clicked close
                running = False # Flag that we are done so we exit this loop
        if keyspressed[ord("\x1b")]: # Pressing the x Key will quit the game
                running = False             
        if keyspressed[ord("a")]:
            x2 -= move
            print("can press")
        if keyspressed[ord("d")]:
            x2 += move
        
        if not(jump):
            if keyspressed[ord("w")] or keyspressed[ord(" ")]:
                jump = True
        else:
            if jump_count >= -10:
                neg = 1
                if jump_count < 0:
                    neg = -1
                y2 = y2 - (jump_count**2)* grav * neg
                jump_count -= 1
            else:
                jump = False
                jump_count = 10
            
        if y2 < 0: 
            y2 = 0
        if y2 >= surface.get_height()-110: 
            y2 = surface.get_height()-110
        if x2 < 400: 
            x2 = 400
        if x2 >= surface.get_width()-50: 
            x2 = surface.get_width()-50   
        

        
        player2 = Rect(x2, y2, 50, 80)
        pygame.draw.rect(surface, (0,0,255), player2)   

        player1 = Rect(x1, y1, 50, 80)
        pygame.draw.rect(surface, (204,0,255), player1)

        send_data = '{}-{}'.format(x2, y2).encode()       # Use format string to enable encode function
        server.send(send_data)

        
        pygame.display.update()                         # Actually does the screen update
        clock.tick(30)                                  # Run the game at 25 frames per second  
        
menu_widgth, menu_height = 400, 250
menu = pygame_menu.Menu('Pikachu',menu_widgth,menu_height ,theme = pygame_menu.themes.THEME_DARK)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(surface)

# Declare grid
#grid = Grid()