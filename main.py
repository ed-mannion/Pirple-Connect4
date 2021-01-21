'''
Project 1:

Connect 4 game
'''

from termcolor import colored, cprint
from random import randint

player1_token = "X"
player2_token = "O"

# Build the starting board.
def build_board():
    board = []
    for row in range(8):
        comumn = []
        if row == 0: 
            for col in range(15):
                if col % 2 == 0:
                    comumn.append("  ")
                else:
                    comumn.append(str(int(col / 2 ) +1 ) + " ")
            board.append(comumn)
        elif row == 1:
            for col in range(15):
                if col % 2 == 0:
                    comumn.append(colored("  ", "blue"))
                else:
                    comumn.append(colored("_ ", "blue"))
            board.append(comumn)            
        else:
            for col in range(15):
                if col % 2 == 0:
                    comumn.append(colored("| ", "blue"))
                else:
                    comumn.append(colored("_ ", "blue"))
            board.append(comumn) 
    return board

# Print the board to the terminal
def print_board(board):
    for row in range(len(board)):
        for column in range(len(board[row])):
            if column == 14:
                print(board[row][column])
            elif board[row][column] == "X":
                piece = colored(u'\u2B24', "red")
                print(piece + " ", end="")
            elif board[row][column] == "O":
                piece = colored(u'\u2B24', "yellow")
                print(piece + " ", end="")
            else:
                print(board[row][column], end="")

# Check to see if a winning condition exists in the sliced up board
def check_win(sliced_board):
    if ["X","X","X","X"] in sliced_board:
        return "p1_wins"
    elif ["O","O","O","O"] in sliced_board:
        return "p2_wins"
    else:
        return "no_winner"

# As the board is built top-down rather than bottom-up and the move should be added to the end of the column
def update_board(board, player, row, column):
    new_board = board
    if player == 1:
        new_board[-row][column] = player1_token
    else:
        new_board[-row][column] = player2_token
    return new_board


# Carve the board into horizontal slices of 4 tokens
def slice_horizontally():
    horizontal_slices = []
    for row in range(1,8):
        for col in range(0,4):
            horizontal_sub_slice =[]
            for item in range(1,5):
                horizontal_sub_slice.append(current_board[row][int((item+col)*2)-1])
            horizontal_slices.append(horizontal_sub_slice)
    return horizontal_slices

# Carve the board into vertical slices of 4 tokens
def slice_vertically():
    vertical_slice = []
    for col in range(1,14,2):
        for row in range(4):
            vertical_sub_slice = []
            for item in range(1,5):
                vertical_sub_slice.append(current_board[item + row][col])
            vertical_slice.append(vertical_sub_slice)
    return vertical_slice

# Carve the board into upward diagonal (/) slices of 4 tokens
def slice_forward_diagonal():
    forward_diagonal = []
    for row in range(0,4):
        for col in range(0,4):
            forward_diagonal_sub = []
            for item in range(1,5):
                forward_diagonal_sub.append(current_board[-(col+item)][int(((item+row)*2)-1)])
            forward_diagonal.append(forward_diagonal_sub)
    return forward_diagonal

# Carve the board into downward diagonal (\) slices of 4 tokens
def slice_downward_diagonal():
    downward_diagonal = []
    for row in range(0,4):
        for col in range(0,4):
            downward_diagonal_sub = []
            for item in range(1,5):
                downward_diagonal_sub.append(current_board[col+item][int(((item+row)*2)-1)])
            downward_diagonal.append(downward_diagonal_sub)
    return downward_diagonal

# For neatness the playable columns are 1-7, however the board is twice that. So a move needs to be adjusted 
def adjust_move(move):
    adjusted_move = (move * 2) - 1
    return adjusted_move

def set_token(turn):
    if turn % 2 == 0:
        token = player1_token
        player = "Player 1"
    else:
        token = player2_token
        player = "Player 2"
    return token, player

def play_move(turn):
    # start at the bottom of the board as game is played bottom-up
    row = 7
    valid_move = False
    move_completed = False
    token, player = set_token(turn)
    
    # Check input is an integer between 1 and 7 and that the chosen column isn't full    
    while valid_move == False:    
        played_col = input(f"{player} please choose a column to play: " )
        if played_col.isdigit() == False:
            print("Must be a number between 1 and 7")
        elif int(played_col) < 1 or int(played_col) > 7:
            print("Must be a number between 1 and 7")
        elif current_board[2][adjust_move(int(played_col))] != (colored("_ ", "blue")):
            print("Can't choose a full column!")
        else:
            col = adjust_move(int(played_col))
            valid_move = True

    # Drop piece into next empty slot (vertically)
    while move_completed == False:
        if current_board[row][col] != colored("_ ", "blue"):
            row -= 1
        # if the move is accepted move to next player's turn
        else:
            current_board[row][col] = token
            move_completed = True

'''
Play the game!
'''

current_board = build_board()
print_board(current_board)
we_have_a_winner = False
turn = 0

while we_have_a_winner == False:
    play_move(turn)
    print_board(current_board)
    if check_win(slice_downward_diagonal()) == "p1_wins" or check_win(slice_forward_diagonal()) == "p1_wins" or check_win(slice_horizontally()) == "p1_wins" or check_win(slice_vertically()) == "p1_wins":
        print("Player 1 Wins!")
        we_have_a_winner = True
    elif check_win(slice_downward_diagonal()) == "p2_wins" or check_win(slice_forward_diagonal()) == "p2_wins" or check_win(slice_horizontally()) == "p2_wins" or check_win(slice_vertically()) == "p2_wins":
        print("Player 2 Wins!")
        we_have_a_winner = True
    turn += 1
    print("\n\n")
