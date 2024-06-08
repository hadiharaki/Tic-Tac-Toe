import sys
import pygame 
import numpy as np 

pygame.init()

#Define colors

WHITE=(255,255,255) #default color
GRAY=(180,180,180) #tie color
RED=(255,0,0) #255 maxing red, lose color
GREEN=(0,255,0) #win color
BLACK=(0,0,0) #background

#Proportions and sizes

WIDTH=300 #width of the window game
HEIGHT=300 
LINE_WIDTH=5  #width of the grid lines
BOARD_ROWS=3 # 3 rows
BOARD_COLS=3 # 3 columns
SQUARE_SIZE= WIDTH // BOARD_COLS # width of the whole screen divided by how many columns we have OR rows because the are the same
CIRCLE_RADIUS= SQUARE_SIZE //3 # the circle radius that is for the player icon O is square size divided by 3 just to fit in the square
CIRCLE_WIDTH=15 #width of the circle line
CROSS_WIDTH= 25 #width of the cross lines


screen= pygame.display.set_mode((WIDTH,HEIGHT)) #creating screen object, this intialize a screen 300x300
pygame.display.set_caption('Tic Tac Toe ') #setting the title
screen.fill(BLACK) #filling the screen with black
board = np.zeros((BOARD_ROWS,BOARD_COLS)) #we define the structure, so it will be 3 by 3 full of zeros and zero mean that no one have played yet on the field

# this function will be called when we want to draw lines ex: at the start of the game, when win, lose or tie
def draw_lines(color=WHITE): 
    # this function will draw the lines of the board with a default color white so we can pass different colors when lose red , win green, tie grey
    for i in range(1,BOARD_ROWS):
        #from 1 to the number of rows, here we want 2 lines vertically and 2 horizontally
        pygame.draw.line(screen,color,(0,SQUARE_SIZE*i),(WIDTH,SQUARE_SIZE*i),LINE_WIDTH) # from start 0 to the end width this draw it horizontally
        pygame.draw.line(screen,color,(SQUARE_SIZE*i,0),(SQUARE_SIZE*i,HEIGHT),LINE_WIDTH) # from 0 to the Height this draw it vertically
        
        
#The function draw figures checks the information on the board if we have all zeros so we dont have to do anything
# ones or twos, ones indicating the player and twos for the AI and then mark these positions on the board
def draw_figures(color=WHITE): #White is default
    #checking the cols of all the rows to know what in have 0,1 or 2
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col]==1: #1 is the player so we have to plot a circle
                pygame.draw.circle(screen,color,(int(col*SQUARE_SIZE + SQUARE_SIZE//2),int(row*SQUARE_SIZE+SQUARE_SIZE//2)),CIRCLE_RADIUS,CIRCLE_WIDTH) # int is the position (col*square size) is to get in the right column + squaresize/2 to be in the center of this specific square and the same of the row (horizontally and veritically this is why we do it for col and row)
                # so we draw a circle of the screen with the color, go to the respective row and col (which is the cell or square) and then go to the center of the square horizontally and vertically and draw the circlw with its width and radius
            elif board[row][col]==2: #if we have 2 instead of 1 in this position we want to draw an X since it is for the AI
                pygame.draw.line(screen,color,(col*SQUARE_SIZE+SQUARE_SIZE//4,row*SQUARE_SIZE+SQUARE_SIZE//4),(col*SQUARE_SIZE+3*SQUARE_SIZE//4,row*SQUARE_SIZE+3*SQUARE_SIZE//4),CROSS_WIDTH) #draw.line because we want to draw 2 crossed lines, starting pos is col*square size and we want to go from one corner to the end corner so + squaresize//4
                    # we go to square and go the one forth of it so on the top left and then go to the three forth of the cell so bottom right corner (this for the starting position:col*SQUARE_SIZE+SQUARE_SIZE//4,row*SQUARE_SIZE+SQUARE_SIZE//4)
                    #and then the end position so by that we drawed on line for the second line: 
                pygame.draw.line(screen,color,(col*SQUARE_SIZE+SQUARE_SIZE//4,row*SQUARE_SIZE+3*SQUARE_SIZE//4),(col*SQUARE_SIZE+3*SQUARE_SIZE//4,row*SQUARE_SIZE+SQUARE_SIZE//4),CROSS_WIDTH)
                #this second line is from the top right to the bottom left
            
def mark_square(row,col,player):
    board[row][col]=player #take the board at position row and col and set it to the player number so that what the function does

def available_square(row,col):
    return board[row][col]==0 #this function return if the cell is played or not if 1,2 it is played by player or AI , 0 it is not played by anyone


def is_board_full(check_board=board): # check if any space left on the board, it is by default board but we can change it and use any future board instead of the default board
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if check_board[row][col]==0: #there is unplayed cells
                return False
    return True #full board

#this function check if someone is won according to the tictactoe rules (3 in a row, 3 in a col, or diagnol is the same)
def check_win(player,check_board=board): #checking a win for player(1 or 2) and board is by default (can be changed) 
    for col in range(BOARD_COLS):
        if check_board[0][col]==player and check_board[1][col]==player and check_board[2][col]==player: #checking if all the column different rows (vertically) is the same so player win 
            return True #so player win
        
    for row in range(BOARD_ROWS):
        if check_board[row][0]==player and check_board[row][1]==player and check_board[row][2]==player: #checking if all the row different columns (horizontally) is the same so player win 
            return True #so player win
        
    if check_board[0][0]==player and check_board[1][1]==player and check_board[2][2]==player: #checking the diagonal from top left to bottom right if it is the same if yes the player win
        return True
    
    if check_board[0][2]==player and check_board[1][1]==player and check_board[2][0]==player: #checking the diagonal from top right to bottom left if it is the same if yes the player win
        return True
    
    return False # not yet anyone won


def minimax(minimax_board,depth,is_maximizing): #ismax is boolean
    #this function is how the AI makes decission
    #we have a base case which is the end (win,lose,tie)
    if check_win(2,minimax_board): #2 is the AI, give it the board in the parameter, if computer win we give the computer the best score because win is the best thing could happen so infinite score
        return float('inf')
    elif check_win(1,minimax_board): #1 is the player, if the player won so the computer lost and it is the worst thing could happen so the computer take the worst score which is -infinity
        return float('-inf')
    elif is_board_full(minimax_board): #the board is full and no one won so it is a tie this is not good and not bad so the score will be 0
        return 0
    
    #the AI take all the possibilities and give each one a score to respond to my move with the best possibility
    if is_maximizing: #if is_maximizing the computer is simulating its own move, deciding what it should do and what is the best move for him
        best_score=-1000 #we took it like this so we can easily beat it
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS): #we try all the possibilities
                if minimax_board[row][col]==0: #we consider first of all all the cells that are available
                    minimax_board[row][col]=2 #simulate what could happen if we play in this cell(computer play X in this cell)
                    score= minimax(minimax_board,depth+1,False) #we calculate the score of this action by recursively calling the minimax function and we increase the depth by 1 to go deeper amd is_maximizing here is false because the next step the player will play and the player tries to decrease the computer score
                    #so here we were maximizing my score because the computer is playing but when the player is playing we are not maximizing because the computer should think what the player would do and what is the worst thing the player could do against the computer
                    #so the computer is decreasing his score. so to simulate what the player would do the computer should think like the player and make the move that is worst for him
                    #it goes back and forth in this recursion untill a base case and do that for all the different possibilities
                    minimax_board[row][col]=0 #setting ity back to zero as if nothing happend
                    best_score=max(score,best_score) # the best score is the maximum between the score and the best score that i already have from the previous possibilities
        return best_score 
    else:
        #here we are trying to minimize the score and when we minimize we take the best desicion for the player and the worst decision for the computer
        best_score= 1000 
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS): #we try all the possibilities
                if minimax_board[row][col]==0: #we consider first of all all the cells that are available
                    minimax_board[row][col]=1 #the player turn now
                    score= minimax(minimax_board,depth+1,True) 
                    minimax_board[row][col]=0 #setting ity back to zero as if nothing happend
                    best_score=min(score,best_score) # the best score is the maximum between the score and the best score that i already have from the previous possibilities
        return best_score 
    #in the first the AI looks at all the free cells and ask what happen if the computer choose this cell,what would the enemy do, and it evaluate what will the oponent will do is by calling the function recursively from the another perspective (minimizing)
    #else it pretends to be the player, the player want to minimize the score for the AI,it consider all the free fields and consider what the AI will do as a response (maximizing True) and go back and forth untill a base case
    
def best_move():#uses the minimax function to decide what is the best move
    best_score=-1000
    move=(-1,-1) #move by default is -1,-1 the move is the cell that we will choose
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col]==0: #then the AI will consider what happens when the cell is set to 2
                board[row][col]=2 #this the move that AI do
                score=minimax(board,0,False) #we call the minimax with the original board with depth of 0 and not maximizing bcz this call of the function will evaluate the possibile moves of the oponent(player)
                board[row][col]=0
                if score>best_score:
                    best_score=score
                    move=(row,col) #this is the position of the cell we want to choose
    if move !=(-1,-1):
        mark_square(move[0],move[1],2)
        return True
    return False
#function to restart the game
def restart_game():
    screen.fill(BLACK) #fill the screen with black color
    draw_lines() #draw the lines again
    for row in range (BOARD_ROWS):
        for col in range (BOARD_COLS):
            board[row][col]=0 #setting all the values of the cells into zeros again
            
#we will start the game
draw_lines() #we draw the lines of the grid
player =1 #we define which player is starting the play
game_over=False #the game is not over yet we just started
 
#start our main loop
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit() #exit the game
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over: #so when we click and game is not over   
            #we get the coordinates of the mouse clicked to determine which cell is clicked and set if it is free the symbol
            mouseX= event.pos[0]// SQUARE_SIZE
            mouseY= event.pos[1]//SQUARE_SIZE
            
            if available_square(mouseY,mouseX):
                mark_square(mouseY,mouseX,player)
                if check_win(player): #if the player won and the game is over gameover will be true else we change the player and player%2+1 turn 1 to 2
                    game_over=True
                player=player%2+1 #1%2=1+1=2
                if not game_over: #if the game is not over after this move we get the best move of the computer
                    if best_move(): #we take the best move of the computer, if best_move() check if the computer did a move and by calling this function in the if condition the computer will do a move
                        #if there is a move that is made we check if this result is a win for the computer if yes game over if not change the player
                        if check_win(2):
                            game_over=True
                        player=player%2+1
                
                if not game_over: #we check after the computer played and AI played and the game is not over it may be a tie so we check if the board is full
                    if is_board_full():
                        game_over=True
                
        if event.type== pygame.KEYDOWN:
            if event.key== pygame.K_r:
                restart_game()
                game_over=False
                player=1
    if not game_over: #if the game is not ended so we draw the figures/update the board information since we have numbers in the cells 0,1,2 using mark_square that assign numbers to the cells and draw figures draw O or X according to the number in the cell
        draw_figures()
        #if the game is over we check for win lose or tie and draw the lines and figures with their colors
    else:
        if check_win(1): #if 1 (player) win we draw in green
            draw_figures(GREEN)
            draw_lines(GREEN)
            
        elif check_win(2): #Computer Win 
            draw_figures(RED)
            draw_lines(RED)
        
        else:
            draw_figures(GRAY)
            draw_lines(GRAY)   
            
    pygame.display.update()     