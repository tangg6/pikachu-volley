import pygame
import pygame_menu
from pygame.locals import *

pygame.init()

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '1000,200'

import threading

# ----------------------- Function to create thread -----------------

def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True # Use deamon thread
    thread.start()

#------------------------ Connect to server  ------------------------------

import socket

HOST = '127.0.0.1'
PORT = 62107
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
server.connect((HOST,PORT))         # Connect


#------------------------- Recieve data from server --------------------------------

def recieve_data():
    global x1,y1,pos_x,pos_y,score_player1,score_player2
    while True:
        data = server.recv(1024).decode()
        data = data.split('-')
        x1, y1 = float(data[0]), float(data[1])
        if data[2] != '':                                   # To fix bug 
            pos_x, pos_y = float(data[2]), float(data[3])
            score_player1,score_player2 = data[4], data[5]

#------------------------ Another thread doing about server ------------------------------

create_thread(recieve_data)

#------------------------- Create a display of game ---------------------------------

size_game = (g_width,g_height) = (800,600)
surface = pygame.display.set_mode(size_game)
pygame.display.set_caption("Pikachu Volley") 
icon = pygame.image.load(os.path.join('src','icon.png'))
pygame.display.set_icon (icon)
clock = pygame.time.Clock() 

#------------------------ Declare values before recieve from client ----------------

x1, y1 = 50, 490                        # Declare position of player 1 before recieve position from server
pos_x, pos_y = 40, 40                   # Declare position of ball before recieve position from server
block_size = 60         
score_player1,score_player2 = '0','0'   # Declare score before recieve position from server


#----------------------------------- Main -------------------------------------------

def start_the_game():
    running = True

    x2, y2 = 675, 500   # Initial position of player 2

    # Detail of player 
    move = 20               # Speed of player 
    jump = False            # To check player jumping?
    jump_count = 10         # State of jumping
    grav = 0.5              # Gravity

    # Import background in to game
    surface = pygame.display.set_mode(size_game)
    bg = pygame.image.load(os.path.join('src','pikachu_background.png'))

    # Import image of player, ball
    img_ball = pygame.image.load(os.path.join('src','ball.png'))
    img_player1 = pygame.image.load(os.path.join('src','pika.png'))
    img_player2 = pygame.image.load(os.path.join('src','pika2.png'))

    
    #------------------- Game when create server and client connected --------------
    while running:
        
        # -------------- Condtion before get into the game ------------
        keyspressed = pygame.key.get_pressed()
        for event in pygame.event.get():            # User did something 
            if event.type == pygame.QUIT:           # If user clicked exit
                running = False                     # End the loop


        # ------------------ Make a shape of player --------
        player2 = Rect(x2, y2, 50, 80)
        player1 = Rect(x1, y1, 50, 80)

        # --------------------- Making a ball -----------------------------
        ball = Rect(pos_x,pos_y,block_size,block_size)

        # ---------------------- Input background ----------
        surface.blit(bg, (0, 0))


        # -------------- Pressing the ESC Key to quit the game --------
        if keyspressed[ord("\x1b")]: 
                running = False        


        # ------- Moving player ----------
        if keyspressed[ord("a")]:                   # Pressing A to move left
            x2 -= move
        if keyspressed[ord("d")]:                   # Pressing D to move right
            x2 += move
        if not(jump):                               # Pressing W or Spacebar to jump
            if keyspressed[ord("w")] \
            or keyspressed[ord(" ")]:
                jump = True                         # If jump = True we will calculate Gravity
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
        

        #---------------- Detect player won't out of bound --------------
        if y2 < 0: 
            y2 = 0
        if y2 >= surface.get_height()-110: 
            y2 = surface.get_height()-110
        if x2 < 405: 
            x2 = 405
        if x2 >= surface.get_width()-70: 
            x2 = surface.get_width()-70   
        
    


        # ------------------------ Display Objective --------------------------
        surface.blit(img_ball,ball.topleft)       # Display ball as Pokeball
        surface.blit(img_player1,player1.topleft) # Draw player1 as pikachu 
        surface.blit(img_player2,player2.topleft) # Draw player2 as pikachu 
        

        # ------------------------ Display score ------------------------------
        font = pygame.font.Font(os.path.join('src', 'GenericMobileSystem.ttf'), 50)
        text_score_player1 = font.render(score_player1, False, (255, 0, 0))
        text_score_player2 = font.render(score_player2, False, (255, 0, 0))      
        surface.blit(text_score_player1, (180,60))
        surface.blit(text_score_player2, (620,60))


        # ------------------------ Send data to server ------------------------
        send_data = '{}-{}'.format(x2, y2).encode()       # Use format string to enable encode function
        server.send(send_data)


        pygame.display.update()                         # Actually does the screen update
        clock.tick(30)                                  # Run the game at 30 frames per second  
        
#------------------------ Menu before enter to the game --------------------------
menu_widgth, menu_height = 400, 250
mytheme = pygame_menu.themes.THEME_SOLARIZED.copy()
mytheme.title_background_color=(230, 242, 255)
menu = pygame_menu.Menu('Pikachu',menu_widgth,menu_height ,theme = mytheme)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(surface)