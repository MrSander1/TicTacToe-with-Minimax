import pygame
import sys
import random
import time

from pygame.locals import *

run = True 
pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("TicTacToe")

clock = pygame.time.Clock()


clicked = False

TTT_images_names = ['X','O']
TTT_images = {}
for name in TTT_images_names:
    filename = 'C:\\TicTacToe\\assets\\' + name + '.png'
    TTT_images[name] = pygame.image.load(filename).convert_alpha()

# Icons
X = TTT_images['X']
X = pygame.transform.scale(X, (150,150))
O = TTT_images['O']
O = pygame.transform.scale(O, (150,150))


grid_size = 3
player_Choice = "X"
opponent_Choice = "O"

# Text Font 
text_font = pygame.font.SysFont("Arial", 90)

# Function that draws text
def draw_text(text, font, text_col, x_pos, y_pos,):
    img = font.render(text, True, text_col)
    SCREEN.blit(img, (x_pos, y_pos))

# Hitboxes List
hitbox_list = []
for y in range(grid_size):
    row = []
    for x in range(grid_size):
        row.append(pygame.Rect(300 + x * 200, 100 + y * 168, 198, 164))
    hitbox_list.append(row)

def isMovesLeft(board):
   for i in range(grid_size):
      for j in range(grid_size):
         if (board[i][j] == None):
            return True
   return False 
 
# Evaluates the board and returns a values of 0 if none have won or lost. -10 if player wins (Never happens this game is solved). 10 happens if player loses (Happens if the player makes a mistake)
def evaluate(b):
   # Checks for rows
   for row in range(grid_size):
      if (b[row][0] == b[row][1] and b[row][1] == b[row][2]):
         if (b[row][0] == player_Choice):
            return -10
         elif (b[row][0] == opponent_Choice):
            return 10
   # Checks for collumns 
   for col in range(grid_size): 
      if (b[0][col] == b[1][col] and b[1][col] == b[2][col]):
         if (b[0][col] == player_Choice):
            return -10
         elif (b[0][col] == opponent_Choice):
            return 10
   # Checks for diagonials       
   if (b[0][0] == b[1][1] and b[1][1] == b[2][2]):
      if (b[0][0] == player_Choice):
         return -10
      elif (b[0][0] == opponent_Choice):
         return 10
   if (b[0][2] == b[1][1] and b[1][1] == b[2][0]):
      if (b[0][2] == player_Choice):
         return -10
      elif (b[0][2] == opponent_Choice):
         return 10
   # Else if none have won return 0   
   return 0
# A function that checks if there is a Move Left on board 


# A function that evaluates our board to see a win condtion has been met 
# The minimax function which considers all the possible ways
# our computer can decide and assigns them a value, which then
# it compares depending on if it's on Minimizers Turn or Maximizers Turn
# and returns the value of this given board.    
def minimax(board, depth, isMax):
   score = evaluate(board)
   # If Maximizer has won return it's evaluated score  
   if (score == 10):
      return score
   # If Minimizers has won return it's evaluated score 
   if (score == -10):
      return score
   # If there are no more moves and no winner: tie
   if not isMovesLeft(board):
      return 0

   # If this is the Maximizer's Move
   if (isMax):
      best = -1000
      # Traverse all cells
      for i in range (grid_size):
         for j in range(grid_size):
            # Check if cell is empty
            if (board[i][j] is None):
               # Makes the Move  
                  board[i][j] = opponent_Choice
                  # Call minimax recursively and choose
                  # the Maximum value
                  best = max(best, minimax(board,depth + 1, not isMax))
                  # Undo the move
                  board[i][j] = None
      return best 
      # If Minimizer's move
   else:   
      best = 1000
      # Traverse all cells
      for i in range(grid_size):
         for j in range(grid_size):
            # Check if cell is empty
               if (board[i][j] is None):
                  # Make the move
                  board[i][j] = player_Choice
                  # Call minimax recursively and choose
                  # the minimum value
                  best = min(best,minimax(board, depth + 1, not isMax))
                  # Undo the move
                  board[i][j] = None 
      return best
# This will return the best possible move for the computer   
def findBestMove(board):
   bestVal = -1000
   bestMove = (-2, -2) 

   # Traverse all cells, evaluate minimax function for
   # all empty cells. And return the cell with optimal value
   for i in range(grid_size):
      for j in range(grid_size):    
         # Check if the cell is empty
         if (board[i][j] is None):  
            # Make the move
            board[i][j] = opponent_Choice
            # Compute the evalutation function for this
            # move
            moveVal = minimax(board, 0, False)
            # Undo the move
            board[i][j] = None

            # If the value of the current move is 
            # more than the best value, then update
            # best/
            if (moveVal > bestVal):
               bestMove = (i, j)
               bestVal = moveVal
                   
   return bestMove

# Main Function 

def play():
    # Our Clicked State
    clicked = False
    
    player_Choice = "X"
    opponent_Choice = "O"
    

    board = [
         [ None, None, None], 
         [ None, None, None], 
         [ None, None, None] 
      ]
    
    

    # Main Loop
    while run:  
    # This is our background
        SCREEN.fill("White")
    # This is our timer
        current_time = pygame.time.get_ticks()
        
        

        
        # Grid Lines
        for i in range(grid_size - 1):
           pygame.draw.line(SCREEN, 'Black', ((1350 // 2) - (200 * i), 100), ((1350// 2) - (200 * i), 600),5)
        for i in range(grid_size - 1):
            pygame.draw.line(SCREEN,'Black',(300, (845 // 2) - (166.666666667 * i)),((900, (845 // 2) - (166.666666667 * i))),5)
        
        if clicked == True:
           bestMove = findBestMove(board)


		# Our Control loop
        for event in pygame.event.get():
         if event.type == pygame.QUIT:
             pygame.quit()
             sys.exit()       

         # Our Control 
         if event.type == MOUSEBUTTONDOWN and event.button == 1 and clicked == False:

            print(board)        
            for i in range(grid_size): 
               for j in range(grid_size):
                  if hitbox_list[i][j].collidepoint(event.pos) and board[i][j] == None:
                     board[i][j] = player_Choice
                     clicked = True
         if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if evaluate(board) == 10 or evaluate(board) == -10 or not isMovesLeft(board):
               play()
                  
                            
         if event.type == MOUSEBUTTONUP and event.button == 1 and clicked == True:
            clicked = False   
            
            opponent_Y = bestMove[0]
            opponent_X = bestMove[1]   
             
            board[opponent_Y][opponent_X] = opponent_Choice        
            print("The Optimal Move is :") 
            print("ROW:", bestMove[0], " COL:", bestMove[1])
            print(board)




         
       
        # The loop that draws our X's or O's
        for i in range(grid_size):           
         for value, hitbox in zip(board[i],hitbox_list[i]):
            if value == player_Choice:        
                SCREEN.blit(X,hitbox)
            if value == opponent_Choice and bestMove:
                SCREEN.blit(O,hitbox)
         
        if evaluate(board):
            SCREEN.fill("Red")
            draw_text("You Lose!", text_font, (0,0,0), 480, 260)
            draw_text("Press Space to Try Again", text_font, (0,0,0), 140, 360)
        if evaluate(board) == -10:
            SCREEN.fill("Green")
            draw_text("You Win! How?", text_font, (0,0,0), 480, 260)
            draw_text("Press Space to Try Again", text_font, (0,0,0), 140, 360)
        if isMovesLeft(board) == False:
            SCREEN.fill("Light Grey")
            draw_text("You Tie!", text_font, (0,0,0), 480, 260)
            draw_text("Press Space to Try Again", text_font, (0,0,0), 140, 360)

 
        pygame.display.flip()
        clock.tick(60)
        
                  

play()
    


    


