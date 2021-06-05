import pygame
import pygame_menu
from pygame.locals import *
#from game import Game

pygame.init()

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '200,200'

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
conn, addr = None, None # Define connection and address

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print("waiting for connection...")

#------------------------- Recieve data from client --------------------------------

def recieve_data():
    global x2,y2
    while True:
        data = conn.recv(1024).decode()
        data = data.split('-')
        print(data)
        x2, y2 = int(data[0]), int(data[1])

        

#------------------------ Another thread doing about server ------------------------------

def waiting_for_connection():
    global connection_established, conn, addr
    conn, addr = server.accept() # wait for connection 
    print('Connection address:', str(addr)) # show detail of client that connected
    connection_established = True
    recieve_data()

create_thread(waiting_for_connection)

#------------------------- Create a display of game ---------------------------------
size_game = (800,600)
surface = pygame.display.set_mode(size_game)
pygame.display.set_caption("Ball") #caption
# icon = pygame.image.load(os.path.join('games.png'))
# pygame.display.set_icon (icon)
clock = pygame.time.Clock() 
y = surface.get_height()-70


def start_the_game():
    # Main game

    running = True
    x = 375
    y = 520

    x2, y2 = 675,520
    move = 20
    jump = False
    grav = 10

    while running:
        surface = pygame.display.set_mode(size_game)
        keyspressed = pygame.key.get_pressed()
        for event in pygame.event.get(): # User did something
            #print(event)    # Useful debugging tip    
            if event.type == pygame.QUIT: # If user clicked close
                running = False # Flag that we are done so we exit this loop
        if keyspressed[ord("\x1b")]: # Pressing the x Key will quit the game
                running = False             
        if keyspressed[ord("a")]:
            x -= move
        if keyspressed[ord("d")]:
            x += move
        print("x = ",x)
        if not(jump):
            if keyspressed[ord("w")] or keyspressed[ord(" ")]:
                jump = True
        else:
            if grav >= -10:
                neg = 1
                if grav < 0:
                    neg = -1
                y = y - (grav**2)* 0.6 * neg
                grav -= 1
                #print(grav)
                print("y = ",y)
            else:
                jump = False
                grav = 10
            
        if y < 0: 
            y = 0
        if y >= surface.get_height()-80: 
            y = surface.get_height()-80
        if x < 0: 
            x = 0
        if x >= surface.get_width()-450: 
            x = surface.get_width()-450   
        
        player1 = Rect(x, y, 50, 80)
        pygame.draw.rect(surface, (204,0,255), player1)   

        player2 = Rect(x2, y2, 50, 80)
        pygame.draw.rect(surface, (0,0,255), player2)

        send_data = '{}-{}'.format(x, y).encode()       # Use format string to enable encode function
        conn.send(send_data)

        

        pygame.display.update()                         # Actually does the screen update
        clock.tick(30)                                  # Run the game at 25 frames per second  
        
menu_widgth, menu_height = 400, 250
menu = pygame_menu.Menu('Pikachu',menu_widgth,menu_height ,theme = pygame_menu.themes.THEME_DARK)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(surface)

# Declare grid
#grid = Grid()