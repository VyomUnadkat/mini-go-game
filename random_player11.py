from random import choice
import random
import sys
#from read import readInput
#from write import writeOutput
import time
#from host import GO
import math
from copy import deepcopy

import sys
import random
import timeit
import math
import argparse
from collections import Counter
from copy import deepcopy

#from read import *
#from write import writeNextInput


#######################################################################################################################################################

class GO:
    def __init__(self, n):
        """
        Go game.

        :param n: size of the board n*n
        """
        self.size = n
        #self.previous_board = None # Store the previous board
        self.X_move = True # X chess plays first
        self.died_pieces = [] # Intialize died pieces to be empty
        self.n_move = 0 # Trace the number of moves
        self.max_move = n * n - 1 # The max movement of a Go game
        self.komi = n/2 # Komi rule
        self.verbose = False # Verbose only when there is a manual player

    def init_board(self, n):
        '''
        Initialize a board with size n*n.

        :param n: width and height of the board.
        :return: None.
        '''
        board = [[0 for x in range(n)] for y in range(n)]  # Empty space marked as 0
        # 'X' pieces marked as 1
        # 'O' pieces marked as 2
        self.board = board
        self.previous_board = deepcopy(board)

    def set_board(self, piece_type, previous_board, board):
        '''
        Initialize board status.
        :param previous_board: previous board state.
        :param board: current board state.
        :return: None.
        '''

        # 'X' pieces marked as 1
        # 'O' pieces marked as 2

        for i in range(self.size):
            for j in range(self.size):
                if previous_board[i][j] == piece_type and board[i][j] != piece_type:
                    self.died_pieces.append((i, j))

        # self.piece_type = piece_type
        self.previous_board = previous_board
        self.board = board

    def compare_board(self, board1, board2):
        for i in range(self.size):
            for j in range(self.size):
                if board1[i][j] != board2[i][j]:
                    return False
        return True

    def copy_board(self):
        '''
        Copy the current board for potential testing.

        :param: None.
        :return: the copied board instance.
        '''
        return deepcopy(self)

    def detect_neighbor(self, i, j):
        '''
        Detect all the neighbors of a given stone.

        :param i: row number of the board.
        :param j: column number of the board.
        :return: a list containing the neighbors row and column (row, column) of position (i, j).
        '''
        board = self.board
        neighbors = []
        # Detect borders and add neighbor coordinates
        if i > 0: neighbors.append((i-1, j))
        if i < len(board) - 1: neighbors.append((i+1, j))
        if j > 0: neighbors.append((i, j-1))
        if j < len(board) - 1: neighbors.append((i, j+1))
        return neighbors

    def detect_neighbor_ally(self, i, j):
        '''
        Detect the neighbor allies of a given stone.

        :param i: row number of the board.
        :param j: column number of the board.
        :return: a list containing the neighbored allies row and column (row, column) of position (i, j).
        '''
        board = self.board
        neighbors = self.detect_neighbor(i, j)  # Detect neighbors
        group_allies = []
        # Iterate through neighbors
        for piece in neighbors:
            # Add to allies list if having the same color
            if board[piece[0]][piece[1]] == board[i][j]:
                group_allies.append(piece)
        return group_allies

    def ally_dfs(self, i, j):
        '''
        Using DFS to search for all allies of a given stone.

        :param i: row number of the board.
        :param j: column number of the board.
        :return: a list containing the all allies row and column (row, column) of position (i, j).
        '''
        stack = [(i, j)]  # stack for DFS serach
        ally_members = []  # record allies positions during the search
        while stack:
            piece = stack.pop()
            ally_members.append(piece)
            neighbor_allies = self.detect_neighbor_ally(piece[0], piece[1])
            for ally in neighbor_allies:
                if ally not in stack and ally not in ally_members:
                    stack.append(ally)
        return ally_members

    def find_liberty(self, i, j):
        '''
        Find liberty of a given stone. If a group of allied stones has no liberty, they all die.

        :param i: row number of the board.
        :param j: column number of the board.
        :return: boolean indicating whether the given stone still has liberty.
        '''
        board = self.board
        ally_members = self.ally_dfs(i, j)
        for member in ally_members:
            neighbors = self.detect_neighbor(member[0], member[1])
            for piece in neighbors:
                # If there is empty space around a piece, it has liberty
                if board[piece[0]][piece[1]] == 0:
                    return True
        # If none of the pieces in a allied group has an empty space, it has no liberty
        return False

    def find_died_pieces(self, piece_type):
        '''
        Find the died stones that has no liberty in the board for a given piece type.

        :param piece_type: 1('X') or 2('O').
        :return: a list containing the dead pieces row and column(row, column).
        '''
        board = self.board
        died_pieces = []

        for i in range(len(board)):
            for j in range(len(board)):
                # Check if there is a piece at this position:
                if board[i][j] == piece_type:
                    # The piece die if it has no liberty
                    if not self.find_liberty(i, j):
                        died_pieces.append((i,j))
        return died_pieces

    def remove_died_pieces(self, piece_type):
        '''
        Remove the dead stones in the board.

        :param piece_type: 1('X') or 2('O').
        :return: locations of dead pieces.
        '''

        died_pieces = self.find_died_pieces(piece_type)
        if not died_pieces: return []
        self.remove_certain_pieces(died_pieces)
        return died_pieces

    def remove_certain_pieces(self, positions):
        '''
        Remove the stones of certain locations.

        :param positions: a list containing the pieces to be removed row and column(row, column)
        :return: None.
        '''
        board = self.board
        for piece in positions:
            board[piece[0]][piece[1]] = 0
        self.update_board(board)

    def place_chess(self, i, j, piece_type):
        '''
        Place a chess stone in the board.

        :param i: row number of the board.
        :param j: column number of the board.
        :param piece_type: 1('X') or 2('O').
        :return: boolean indicating whether the placement is valid.
        '''
        board = self.board

        valid_place = self.valid_place_check(i, j, piece_type)
        if not valid_place:
            return False
        self.previous_board = deepcopy(board)
        board[i][j] = piece_type
        self.update_board(board)
        # Remove the following line for HW2 CS561 S2020
        # self.n_move += 1
        return True

    def valid_place_check(self, i, j, piece_type, test_check=False):
        '''
        Check whether a placement is valid.

        :param i: row number of the board.
        :param j: column number of the board.
        :param piece_type: 1(white piece) or 2(black piece).
        :param test_check: boolean if it's a test check.
        :return: boolean indicating whether the placement is valid.
        '''   
        board = self.board
        verbose = self.verbose
        if test_check:
            verbose = False

        # Check if the place is in the board range
        if not (i >= 0 and i < len(board)):
            if verbose:
                print(('Invalid placement. row should be in the range 1 to {}.').format(len(board) - 1))
            return False
        if not (j >= 0 and j < len(board)):
            if verbose:
                print(('Invalid placement. column should be in the range 1 to {}.').format(len(board) - 1))
            return False
        
        # Check if the place already has a piece
        if board[i][j] != 0:
            if verbose:
                print('Invalid placement. There is already a chess in this position.')
            return False
        
        # Copy the board for testing
        test_go = self.copy_board()
        test_board = test_go.board

        # Check if the place has liberty
        test_board[i][j] = piece_type
        test_go.update_board(test_board)
        if test_go.find_liberty(i, j):
            return True

        # If not, remove the died pieces of opponent and check again
        test_go.remove_died_pieces(3 - piece_type)
        if not test_go.find_liberty(i, j):
            if verbose:
                print('Invalid placement. No liberty found in this position.')
            return False

        # Check special case: repeat placement causing the repeat board state (KO rule)
        else:
            if self.died_pieces and self.compare_board(self.previous_board, test_go.board):
                if verbose:
                    print('Invalid placement. A repeat move not permitted by the KO rule.')
                return False
        return True
        
    def update_board(self, new_board):
        '''
        Update the board with new_board

        :param new_board: new board.
        :return: None.
        '''   
        self.board = new_board

    def visualize_board(self):
        '''
        Visualize the board.

        :return: None
        '''
        board = self.board

        print('-' * len(board) * 2)
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 0:
                    print(' ', end=' ')
                elif board[i][j] == 1:
                    print('X', end=' ')
                else:
                    print('O', end=' ')
            print()
        print('-' * len(board) * 2)

    def game_end(self, piece_type, action="MOVE"):
        '''
        Check if the game should end.

        :param piece_type: 1('X') or 2('O').
        :param action: "MOVE" or "PASS".
        :return: boolean indicating whether the game should end.
        '''

        # Case 1: max move reached
        if self.n_move >= self.max_move:
            return True
        # Case 2: two players all pass the move.
        if self.compare_board(self.previous_board, self.board) and action == "PASS":
            return True
        return False

    def score(self, piece_type):
        '''
        Get score of a player by counting the number of stones.

        :param piece_type: 1('X') or 2('O').
        :return: boolean indicating whether the game should end.
        '''

        board = self.board
        cnt = 0
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == piece_type:
                    cnt += 1
        return cnt          

    def judge_winner(self):
        '''
        Judge the winner of the game by number of pieces for each player.

        :param: None.
        :return: piece type of winner of the game (0 if it's a tie).
        '''        

        cnt_1 = self.score(1)
        cnt_2 = self.score(2)
        if cnt_1 > cnt_2 + self.komi: return 1
        elif cnt_1 < cnt_2 + self.komi: return 2
        else: return 0
        
    def play(self, player1, player2, verbose=False):
        '''
        The game starts!

        :param player1: Player instance.
        :param player2: Player instance.
        :param verbose: whether print input hint and error information
        :return: piece type of winner of the game (0 if it's a tie).
        '''
        self.init_board(self.size)
        # Print input hints and error message if there is a manual player
        if player1.type == 'manual' or player2.type == 'manual':
            self.verbose = True
            print('----------Input "exit" to exit the program----------')
            print('X stands for black chess, O stands for white chess.')
            self.visualize_board()
        
        verbose = self.verbose
        # Game starts!
        while 1:
            piece_type = 1 if self.X_move else 2

            # Judge if the game should end
            if self.game_end(piece_type):       
                result = self.judge_winner()
                if verbose:
                    print('Game ended.')
                    if result == 0: 
                        print('The game is a tie.')
                    else: 
                        print('The winner is {}'.format('X' if result == 1 else 'O'))
                return result

            if verbose:
                player = "X" if piece_type == 1 else "O"
                print(player + " makes move...")

            # Game continues
            if piece_type == 1: action = player1.get_input(self, piece_type)
            else: action = player2.get_input(self, piece_type)

            if verbose:
                player = "X" if piece_type == 1 else "O"
                print(action)

            if action != "PASS":
                # If invalid input, continue the loop. Else it places a chess on the board.
                if not self.place_chess(action[0], action[1], piece_type):
                    if verbose:
                        self.visualize_board() 
                    continue

                self.died_pieces = self.remove_died_pieces(3 - piece_type) # Remove the dead pieces of opponent
            else:
                self.previous_board = deepcopy(self.board)

            if verbose:
                self.visualize_board() # Visualize the board again
                print()

            self.n_move += 1
            self.X_move = not self.X_move # Players take 


#######################################################################################################################################################

def readInput(n, path="input.txt"):

    with open(path, 'r') as f:
        lines = f.readlines()

        piece_type = int(lines[0])

        previous_board = [[int(x) for x in line.rstrip('\n')] for line in lines[1:n+1]]
        board = [[int(x) for x in line.rstrip('\n')] for line in lines[n+1: 2*n+1]]

        return piece_type, previous_board, board

def readOutput(path="output.txt"):
    with open(path, 'r') as f:
        position = f.readline().strip().split(',')

        if position[0] == "PASS":
            return "PASS", -1, -1

        x = int(position[0])
        y = int(position[1])

    return "MOVE", x, y


def writeOutput(result, path="output.txt"):
    res = ""
    if result == "PASS":
    	res = "PASS"
    else:
	    res += str(result[0]) + ',' + str(result[1])

    with open(path, 'w') as f:
        f.write(res)

def writePass(path="output.txt"):
	with open(path, 'w') as f:
		f.write("PASS")

def writeNextInput(piece_type, previous_board, board, path="input.txt"):
	res = ""
	res += str(piece_type) + "\n"
	for item in previous_board:
		res += "".join([str(x) for x in item])
		res += "\n"
        
	for item in board:
		res += "".join([str(x) for x in item])
		res += "\n"

	with open(path, 'w') as f:
		f.write(res[:-1]);


def check_board(board, piece_type, x, y):
    print(board)

def evaluate(board, color):
    scoreo, scorex = wins()


    #go.play()
    #print('in evaluate')
    #print('this is the board right now')
    #print(board)
    if piece_type == 1:
    	score = scorex * scorex - scoreo
    if piece_type == 2:
    	score = scoreo * scoreo - scorex
    #print('this is the score for this board')
    #print(score)
    return score

def wins():
	#if piece_type == 2:
		cnt_2 = go.score(2)
		cnt_1 = go.score(1)
		return cnt_2 + go.komi, cnt_1


def empty_cells(board,player):
    possible_placements = []
    for i in range(go.size):
        for j in range(go.size):
            if go.valid_place_check(i, j, player, test_check = True):
                possible_placements.append((i,j))
    random.shuffle(possible_placements)
    return possible_placements

def valid_move(x,y,player):
    if (x,y) in empty_cells(board,player):
        return True
    else:
        return False

def set_move(board, x, y, player):
    if valid_move(x,y, player):
        go.previous_board = deepcopy(board)
        board[x][y] = player
        go.board = board
        return board
    else:
        return board

def minimax_min_node(board, color, depth, alpha, beta, start_time):
    new_board = deepcopy(board)
    # board_to_pass_each_time = deepcopy(board)
    #print('in minimax min')
    #print(new_board)
    cur_min = math.inf
    moves = empty_cells(new_board,color)
    #print(moves)
    #print('depth')
    #print(depth)
    #if depth == 5:
    #	print('please check here')
    #if depth == 4:
    #	print('please check here for depth 4')
    end = time.time()
    if len(moves) == 0 or depth == 0 or end - start_time> 9.5:
        return (-1,-1), evaluate(new_board, color)
    else: 
        for i in moves:
            #print('this is the move')
            #print(i)
            board_to_pass_each_time = deepcopy(board)
            new_board = set_move(board_to_pass_each_time, i[0], i[1], color)
            go.remove_died_pieces(3 - color)
            if color == 1:
                next_player = 2
            else:
                next_player = 1
            new_move, new_score = minimax_max_node(new_board, next_player, depth - 1, alpha, beta, start_time)
            if new_score < cur_min:
                cur_min = new_score
                best_move = i
            beta = min(new_score, beta) 
            if beta <= alpha:
                break
        return best_move, cur_min 

def minimax_max_node(board, color, depth, alpha, beta, start_time):
    end = time.time()
    new_board = deepcopy(board)
    # board_to_pass_each_time = deepcopy(board)
    cur_max = -math.inf
    moves = empty_cells(new_board,color)
    #print('in minimax max')
    #print(board)
    #print(new_board)
    #print(moves)
    #print('depth')
    #print(depth)
    #if depth == 5:
    #	print('please check here')
    #if depth == 4:
    #	print('please check here for depth 4')
    if len(moves) == 0 or depth == 0 or end - start_time> 9.5:
        return (-1,-1), evaluate(new_board, color)
    else: 
        for i in moves:
            #print('this is the move')
            #print(i)
       	    board_to_pass_each_time = deepcopy(board)
            new_board = set_move(board_to_pass_each_time, i[0], i[1], color)
            go.remove_died_pieces(3 - color)
            if color == 1:
                next_player = 2
            else:
                next_player = 1
            new_move, new_score = minimax_min_node(new_board, next_player, depth - 1, alpha, beta, start_time)
            if new_score > cur_max:
                cur_max = new_score
                best_move = i
            alpha = max(new_score, alpha) 
            if beta <= alpha:
                break
        return best_move, cur_max

def select_move_minimax(board, color):
    start = time.time()
    best_move, score = minimax_max_node(board, color, max_depth, -math.inf, math.inf, start )
    i, j = best_move[0], best_move[1]

    return i,j, score



def get_input(go, piece_type):

    moves = empty_cells(go.board,piece_type)
    print('moves')
    print(moves)
    print(len(moves))
    if len(moves) >= 10:
        if (1,1) in empty_cells(go.board, piece_type):
            x = 1
            y = 1
            return (x,y)
        if (1,3) in empty_cells(go.board, piece_type):
            x = 1
            y = 3
            return (x,y)
        if (3,1) in empty_cells(go.board, piece_type):
            x = 3
            y = 1
            return (x,y)
        if (3,3) in empty_cells(go.board, piece_type):
            x = 3
            y = 3
            return (x,y)
        if (2,2) in empty_cells(go.board, piece_type):
            x = 2
            y = 2
            return (x,y)
        if (0,2) in empty_cells(go.board, piece_type):
            x = 0
            y = 2
            return (x,y)
        if (4,2) in empty_cells(go.board, piece_type):
            x = 4
            y = 2
            return (x,y)
        if (2,0) in empty_cells(go.board, piece_type):
            x = 2
            y = 0
            return (x,y)
        if (2,4) in empty_cells(go.board, piece_type):
            x = 2
            y = 4
            return (x,y)
    '''
    if (1,1) in empty_cells(go.board, piece_type):
        x = 1
    	y = 1
    	return (x,y)

    if (1,3) in empty_cells(go.board, piece_type):
    	x = 1
    	y = 3
    	return (x,y)
    if (3,1) in empty_cells(go.board, piece_type):
    	x = 3
    	y = 1
    	return (x,y)
    if (3,3) in empty_cells(go.board, piece_type):
    	x = 3
    	y = 3
    	return (x,y)
    if (2,2) in empty_cells(go.board, piece_type):
    	x = 2
    	y = 2
    	return (x,y)
    if (0,2) in empty_cells(go.board, piece_type):
    	x = 0
    	y = 2
    	return (x,y)
    if (4,2) in empty_cells(go.board, piece_type):
    	x = 4
    	y = 2
    	return (x,y)
    if (2,0) in empty_cells(go.board, piece_type):
    	x = 2
    	y = 0
    	return (x,y)
    if (2,4) in empty_cells(go.board, piece_type):
    	x = 2
    	y = 4
    	return (x,y)
    '''


    movei, movej, score = select_move_minimax(go.board, piece_type)

    x, y = movei, movej

    return(x,y)



N = 5
max_depth = 20
piece_type, previous_board, board = readInput(N)
go = GO(N)
go.set_board(piece_type, previous_board, board)
action = get_input(go, piece_type)
if action == None:
	action = "PASS"
writeOutput(action)
