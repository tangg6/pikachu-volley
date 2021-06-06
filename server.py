import pygame
import pygame_menu
from pygame.locals import *

pygame.init()

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '200,200'

import threading

# ----------------------- Function to create thread -----------------

def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True # Use deamon thread
    thread.start()

#------------------------ Open server ------------------------------

import socket

HOST = '127.0.0.1'
PORT = 62107
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print("waiting for connection...")
conn, addr = server.accept()
print('Client connected by ', str(addr))

#------------------------- Recieve data from client --------------------------------

def recieve_data():
    global x2,y2                                 # Global x2, y2 to change position of player 2
    while True:
        data = conn.recv(1024).decode()
        data = data.split('-')
        x2, y2 = float(data[0]), float(data[1])  # Change value of position player 2

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

x2, y2 = 675, 490           # Declare position of player 2 before recieve position from client


#----------------------------------- Main -------------------------------------------

def start_the_game():
    running = True

    x1, y1 = 50, 490  # Initial position of player 1

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

    # Detail of ball
    block_size = 60         # Size of ball
    x = 5                   # Initial speed of ball in x 
    y = 0                   # Initial speed of ball in y
    friction_x = 1          # Friction when ball bouncing
    pos_x,pos_y  = 40, 40   # Initial position of ball
    
    score_player1 = 0       # Initial score of player 1
    score_player2 = 0       # Initial score of player 2


    #------------------- Game when create server and client connected --------------
    while running:

        # -------------- Condtion before get into the game ------------
        keyspressed = pygame.key.get_pressed()
        for event in pygame.event.get():            # User did something 
            if event.type == pygame.QUIT:           # If user clicked exit
                running = False                     # End the loop


        # ------------------ Make a shape of player --------
        player1 = Rect(x1, y1, 50, 80)
        player2 = Rect(x2, y2, 50, 80)


        # ---------------------- Input background ----------
        surface.blit(bg, (0, 0))


        # -------------- Pressing the ESC Key to quit the game --------
        if keyspressed[ord("\x1b")]: 
                running = False             


        # ------- Moving player ----------
        if keyspressed[ord("a")]:                   # Pressing A to move left
            x1 -= move
        if keyspressed[ord("d")]:                   # Pressing D to move right
            x1 += move
        if not(jump):                               # Pressing W or Spacebar to jump
            if keyspressed[ord("w")] \
            or keyspressed[ord(" ")]:
                jump = True                         # If jump = True we will calculate Gravity
        else:
            if jump_count >= -10:
                neg = 1
                if jump_count < 0:
                    neg = -1
                y1 = y1 - (jump_count**2)* grav * neg
                jump_count -= 1
            else:
                jump = False
                jump_count = 10


        #---------------- Detect player won't out of bound --------------
        if y1 < 0: 
            y1 = 0
        if y1 >= surface.get_height()-110: 
            y1 = surface.get_height()-110
        if x1 < 0:  
            x1 = 0
        if x1 >= surface.get_width()-475: 
            x1 = surface.get_width()-475   

        
        # --------------------- Making a ball -----------------------------
        ball = Rect(pos_x,pos_y,block_size,block_size)
        
        pos_x += x                              # Make the ball moving in x
        pos_y += y                              # Make the ball moving in y


        # ---------------------- The ball hit the wall --------------------
        if pos_y + block_size > g_height and y <= 2.0: 
            x = 0
            y = 0
            grav = 0
            friction_x = 0
        
        if pos_y < 0:                           # If the ball hit the top frame
            y = -y-grav

            
        if pos_x + block_size > g_width or \
            pos_x < 0:                        # If the ball hit the left or right wall
            x = -(x*friction_x)
        
        if pos_x + block_size == g_width // 2 and \
           pos_y + block_size > g_height // 2:
            x = -(x*friction_x)
        if pos_x + block_size == g_width // 2 and \
           pos_y + block_size == g_height // 2:
            y = -y-grav
        

        # --------------------- Ball hit the player floor ------------------------
        # when the player 2 win, the ball will release in player 2 side
        if pos_y + block_size > g_height and \
           pos_x + block_size <= g_width // 2:     
            
            # Reset detail of the ball and release  the ball in player 2 side
            x, y = -5, 0                
            friction_x = 1              
            pos_x, pos_y = 700, 40

            # Plus score to player 2 
            score_player2 += 1
            print("Player1 lose")
        
        # when the player 1 win, the ball will release in player 1 side
        if pos_y + block_size > g_height and \
           pos_x + block_size >= g_width // 2:     

            # Reset detail of the ball and release the ball in player 1 side
            x, y = 5, 0
            friction_x = 1
            pos_x, pos_y = 40, 40

            # Plus score to player 1
            score_player1 += 1
            print("Player2 lose")
        

        # ---------------- Ball hit player ------------------
        if ball.colliderect(player1) and y >= 0 or \
           ball.colliderect(player2) and y >= 0:
            y = -y-grav


        # ------------------------ Display Objective --------------------------
        surface.blit(img_ball,ball.topleft)       # Display ball as Pokeball
        y += grav                                 # When display the ball at first frame
                                                  # then increase speed by gravity
        
        surface.blit(img_player1,player1.topleft) # Display player1 as pikachu
        surface.blit(img_player2,player2.topleft) # Display player2 as pikachu 


        # ------------------------ Display score ------------------------------
        font = pygame.font.Font(os.path.join('src', 'GenericMobileSystem.ttf'), 50)
        text_score_player1 = font.render(str(score_player1), False, (255, 0, 0))
        text_score_player2 = font.render(str(score_player2), False, (255, 0, 0))      
        surface.blit(text_score_player1, (180,60))
        surface.blit(text_score_player2, (620,60))


        # ------------------------ Send data to client ------------------------

        send_data = '{}-{}-{}-{}-{}-{}'.format(x1, y1, pos_x, pos_y, score_player1, score_player2).encode()       # Use format string to enable encode function
        conn.send(send_data)


        pygame.display.update()                    # Actually does the screen update
        clock.tick(30)                             # Run the game at 30 frames per second  
        

#------------------------ Menu before enter to the game --------------------------
menu_widgth, menu_height = 400, 250
menu = pygame_menu.Menu('Pikachu',menu_widgth,menu_height ,theme = pygame_menu.themes.THEME_DARK)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(surface)

