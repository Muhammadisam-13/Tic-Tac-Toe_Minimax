import sys
import pygame
import numpy as np


# A SIMPLE TIC TAC TOE GAME, MADE USING PYGAME AND MINIMAX, 
# TO ALLOW THE USER TO PLAY AGAINST THE COMPUTER

# THIS CODE IS BASED ON THE TUTORIAL "Tic-Tac-Toe Game in Python - Unbeatable Minimax AI", by NeuralNine
# URL: https://youtu.be/LbTu0rwikwg?si=0FSjwP9VuqhGHl13

# My explanation of the minimax algorithm according to my understanding: 

"""
The minimax algorithm is an algorithm that finds the most optimal move against a player, assuming that the player is also playing the best move. 
It is basically a recursive function that recursively moves through all the possibilities in a game, and checks which moves allow it to win, 
assuming that the player is trying to minimize the AI's score as much as possible. This recursive approach creates a game tree containing the 
multiple nodes leading to different outcomes. If it finds, for example, two outcomes leading to a positive score for the AI, it chooses the 
outcome based on the assumption that the player will always choose the best move. The way it checks for a positive outcome for itself is based 
on assigning scores to the outcomes. A draw is 0, a win for the AI is positive infinity, and a win for the player is negative infinity.

"""
# Reference videos used to understand the minimax algorithm:
# Video 1: https://youtu.be/5y2a0Zhgq0U?si=W7zWASmNi65Y5D3_
# Video 2: https://youtu.be/trKjYdBASyQ?si=F6GEiVeIDgy7-kW-

"""
Learning Outcome from this project:
By coding this project, I have learned the working of a widely used algorithm used in many two player games, not just tic-tac-toe. 
I have also further refined my skills in python, and I can now use this knowledge of the minimax algorithm to implement various other 
two-player games such as chess, checkers etc. 

"""


pygame.init()

# colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# CONSTANTS USED THROUGHOUT THE CODE TO IMPLEMENT THE GAME
WIDTH = 450
HEIGHT = 450
LINE_WIDTH = 5
ROWS = 3 # board rows
COLUMNS = 3 # board columns
CIRCLE_WIDTH = 15 # width of the circle
CROSS_WIDTH = 25 # width of the cross
SQUARE_SIZE = WIDTH // COLUMNS
CIRCLE_RADIUS = SQUARE_SIZE // 3

screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Set the screen with a specific width and height
pygame.display.set_caption("TIC TAC TOE WITH MINIMAX AI")

board = np.zeros((ROWS, COLUMNS)) # initialize board list

background_image = pygame.image.load("background.jpg") # background image

# FUNCTIONS USED IN THE GAMEs

def draw_lines(color=WHITE):
    for i in range(1, ROWS):
        pygame.draw.line(screen, color, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, color, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)

def draw_figures(color=WHITE):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, color, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), 
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), CROSS_WIDTH)
                pygame.draw.line(screen, color, (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), CROSS_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col): # checks if the specific square is available
    return board[row][col] == 0

def free_space_available(check_board=board): # returns true if there is free space left in the board (one or more elements in the board list is 0)
    for i in range(ROWS):
        for j in range(COLUMNS):
            if check_board[i][j] == 0:
                return True
    return False

def check_win(player, checkboard=board):
    # Contains all the possible cases in which a player or the AI can win in tic tac toe
    for row in range(ROWS):
            if checkboard[row][0] == player and checkboard[row][1] == player and checkboard[row][2] == player:
                return True
    for col in range(COLUMNS):
            if checkboard[0][col] == player and checkboard[1][col] == player and checkboard[2][col] == player:
                return True   
            
    if checkboard[0][0] == player and checkboard[1][1] == player and checkboard[2][2] == player:
        return True
    
    if checkboard[0][2] == player and checkboard[1][1] == player and checkboard[2][0] == player:
        return True
    
    return False # if none of the cases fulfilled

def minimax(minimax_board, depth, is_maximizing): 
    # implementation of the minimax AI algorithm (Recursive function)

    # Base cases
    if check_win(2, minimax_board):
        return float('inf')
    elif check_win(1, minimax_board):
        return float('-inf')
    elif not free_space_available(minimax_board):
        return 0
    
    # Algorithm logic
    if is_maximizing: # This is true whenever it's the AI's turn, since the AI is trying to maximize its score
        best_score = -10000
        for row in range(ROWS):
            for col in range(COLUMNS):
                if minimax_board[row][col] == 0: #if square is free
                    minimax_board[row][col] = 2 # AI's turn indicated by 2
                    score = minimax(minimax_board, depth + 1, False) # recursive call (is_maximizing passed as false, since next time its the player's turn)
                    minimax_board[row][col] = 0  # update to 0 again while backtracking to ensure no real change occurs as it is for checking
                    best_score = max(score, best_score) # update the best score
        return best_score

    else: # The case fulfilled whenever it's the players turn, since the player is trying to minimize the AI's score
        best_score = 10000
        for row in range(ROWS):
            for col in range(COLUMNS):
                if minimax_board[row][col] == 0: # if square is free
                    minimax_board[row][col] = 1 # player's turn indicated by 1
                    score = minimax(minimax_board, depth + 1, True) # recursive call (is_maximizing passed as true, since next time its the AI's turn)
                    minimax_board[row][col] = 0 # update to 0 again while backtracking to ensure no real change occurs as it is for checking
                    best_score = min(score, best_score) # update the best score
        return best_score
    
def best_move(): # Plays the best possible move found by the minimax algorithm
    best_score = -1000
    move = (-1, -1)
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False) # checks the best move
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
    if move != (-1, -1):
        mark_square(move[0], move[1], player=2)
        return True
    return False
    
def RESTART_GAME(): # press R to restart the game and reset the board
    screen.blit(background_image, (0, 0))
    draw_lines()
    for row in range(ROWS):
        for col in range(COLUMNS):
            board[row][col] = 0


# THE MAIN FUNCTION WHICH CONTAINS THE GAME LOOP 
def PLAY_GAME():
    screen.blit(background_image, (0, 0))   
    draw_lines() 
    player = 1
    game_over = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Check if mouse clicked
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0] // SQUARE_SIZE
                mouseY = event.pos[1] // SQUARE_SIZE

                if available_square(mouseY, mouseX):
                    mark_square(mouseY, mouseX, player)
                    if(check_win(player)):
                        game_over = True
                    player = player % 2 + 1 # converts 1 to 2 and 2 to 1 to alternate turns

                # If the game is not over after player's move, play AI's move and check if the AI won,
                # and if not, then turn alternates again to player
                if not game_over and player == 2:
                    if best_move():
                        if check_win(2):
                            game_over = True
                        player = player % 2 + 1

                # In the case of Tie
                if not game_over: 
                    if not free_space_available():
                        game_over = True

            # If R is clicked, the game restarts
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    RESTART_GAME()
                    game_over = False
                    player = 1
    
        if not game_over:
            draw_figures()
        else:
            if check_win(1):
                draw_figures(GREEN)
                draw_lines(GREEN)
            elif check_win(2):
                draw_figures(RED)
                draw_lines(RED)
            else:
                draw_figures(GRAY)
                draw_lines(GRAY)
            
        pygame.display.update()



PLAY_GAME()