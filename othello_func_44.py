##Othello
##class Board

##Python 3.7.2

import numpy as np
from copy import deepcopy
import random
import sys
#import time


## make initial Othello board
initial_board_44 = np.array([[9,9,9,9,9,9],[9,3,3,3,3,9],[9,3,1,0,3,9],[9,3,0,1,3,9],[9,3,3,3,3,9],[9,9,9,9,9,9]])
# 0 : your disks
# 1 : opponent's disks
# 3 : empty space
# 9 : out of board

##==================
##variables
initial_board = deepcopy(initial_board_44)
BOARD_SIZE = 6
##------------------


class Board():
	def print_board(self,board):
		board = board.astype(np.int64)
		convert_dict = {0:b"\\u25cb", 1:b"\\u25cf", 3:b" ", 9:b""} ## check the color of your terminal window
		converted_board = [[(convert_dict[board[i][j]]).decode('unicode-escape') for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]
		for j in range(BOARD_SIZE):
			print(" ".join(converted_board[j]))

	def playerID_2_disk(self,playerID):
		return playerID, (playerID+1)%2

	def playerID_2_BW(self,playerID):
		BW_dict = {0:'black', 1:'white'}
		return BW_dict[playerID]

	def where_flip_one_direction(self,board,move,direction,flip_arr,playerID):
		your_disk, opponents_disk = self.playerID_2_disk(playerID)
		if board[move[0]+direction[0]][move[1]+direction[1]] == opponents_disk:
			num_flip = 1
			while(True):
				if board[move[0]+(num_flip+1)*direction[0]][move[1]+(num_flip+1)*direction[1]] == opponents_disk:
					num_flip += 1
				elif board[move[0]+(num_flip+1)*direction[0]][move[1]+(num_flip+1)*direction[1]] == your_disk:
					[flip_arr.append([move[0]+k*direction[0],move[1]+k*direction[1]]) for k in range(1,num_flip+1)]
					return flip_arr
					break
				else:
					break
		return flip_arr

	def where_flip_all_direction(self,board,move,playerID):
		arr_direction = np.array([[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]])
		flip_arr = []
		for k in range(8):
			flip_arr = deepcopy(self.where_flip_one_direction(board,move,arr_direction[k].astype(np.int64),flip_arr,playerID))
		return flip_arr

	def flip_board(self,board,move,flip_arr,playerID):
		new_board = deepcopy(board)
		if any(flip_arr):
			new_board[move[0]][move[1]] = playerID
			for i in range(len(flip_arr)):
				new_board[int(flip_arr[i][0])][int(flip_arr[i][1])] = playerID
		return new_board

	def XY_line_to_board(self,XY_line):
		num_move = int(len(XY_line)/2)
		board = deepcopy(initial_board)
		for i in range(num_move):
			move = [int(XY_line[2*i]),int(XY_line[2*i+1])]
			if move == [0,0]:
				continue
			playerID = i%2
			flip = self.where_flip_all_direction(board,move,playerID)
			your_disk, opponents_disk = self.playerID_2_disk(playerID)
			board[move[0]][move[1]] = your_disk
			for i in range(len(flip)):
				board[int(flip[i][0])][int(flip[i][1])] = your_disk
		return board

	def board_to_base10(self,board):
		board = board.astype(np.int64)
		line = ''
		for i in range(1,BOARD_SIZE-1):
			for j in range(1,BOARD_SIZE-1):
				line = line + str(board[i][j])
		base10 = int(line,3)
		return base10

	def base10_to_baseN(self,n,b):
		if (int(n/b)):
			return self.base10_to_baseN(int(n/b), b) + str(n%b)
		return str(n%b)

	def base10_to_board(self,base10):
		line = self.base10_to_baseN(int(base10),3)
		line = '3'*(BOARD_SIZE**2-len(line)) + line
		board = 9 * np.ones((BOARD_SIZE,BOARD_SIZE))
		for i in range(BOARD_SIZE-2):
			for j in range(BOARD_SIZE-1):
				board[i+1][j+1] = line[i*4+j]
		return board

	def is_no_empty(self,board):
		return not (board == 3).any()

	def is_no_opponent(self,board,playerID):
		your_disk, opponents_disk = self.playerID_2_disk(playerID)
		return not (board == opponents_disk).any()

	def is_double_pass_XY(self,pre_XY):
		boolean = (pre_XY[-2:] == '00')
		return boolean

	def is_double_pass_board(self,board):
		for X in range(1,BOARD_SIZE-1):
			for Y in range(1,BOARD_SIZE-1):
				if board[X][Y] != 3:
					continue
				var0 = self.where_flip_all_direction(board,[X,Y],0)
				var1 = self.where_flip_all_direction(board,[X,Y],1)
				if any([len(var0),len(var1)]):
					return False
		return True

	def is_finish_board(self,board):
		return self.is_no_empty(board) or self.is_double_pass_board(board)

	def where_movable(self,board,playerID):
		move_arr = []
		for X in range(1,BOARD_SIZE-1):
			for Y in range(1,BOARD_SIZE-1):
				if board[X][Y] != 3:
					continue
				flip = self.where_flip_all_direction(board,[X,Y],playerID)
				if any(flip):
					move_arr.append([X,Y])
		return move_arr

	def board_2_score(self,board):
		black = np.sum(board == 0)
		white = np.sum(board == 1)
		empty = np.sum(board == 3)
		score = black - white
		return score + (score>0)*empty - (score<0)*empty

	def get_move_from_input(self,board,playerID):
		while True:
			next_move = str(input("type next move >> "))
			if (len(next_move) == 2) and next_move.isdigit():
				X = int(next_move[0])
				Y = int(next_move[1])
				if (X > 0) and (X < 5) and (Y > 0) and (Y < 5):
					flip_arr = self.where_flip_all_direction(board,[X,Y],playerID)
					if (board[X][Y] == 3) and any(flip_arr):
						return [X,Y]
						break
					else:
						print('you cannot move there')
						continue
				else:
					print('type XY (1<=X<=4, 1<=Y<=4)')
					continue
			elif next_move in ["exit","quit"]:
				print('This program was finished ...')
				sys.exit()
			elif next_move == "board":
				self.print_board(board)
				continue
			elif next_move == "where":
				print(self.where_movable(board,playerID))
				continue
			else:
				print('type XY (type ''exit'', then finish)')
				continue
	## improve above def so as to be able to select "matta"

	def play_2players_44(self):
		board = deepcopy(initial_board_44)
		self.print_board(initial_board_44)
		nth_move = 0
		pre_XY = ''
		while True:
			if self.is_finish_board(board):  ##finish
				##result
				print("result")
				score = self.board_2_score(board)
				print('score =', score)
				sys.exit()
			playerID = nth_move%2
			your_disk, opponents_disk = self.playerID_2_disk(playerID)
			print("player: ",self.playerID_2_BW(playerID))
			if not any(self.where_movable(board,playerID)):  ## if pass
				nth_move += 1
				pre_XY += '00'
				print("PASS\n")
				continue
			next_move = self.get_move_from_input(board,playerID)
			flip_arr = self.where_flip_all_direction(board,next_move,playerID)
			board = deepcopy(self.flip_board(board,next_move,flip_arr,playerID))
			self.print_board(board)
			nth_move += 1
			pre_XY += (str(next_move[0])+str(next_move[1]))
			continue


#def make_first_file(self):
#	f_write = open('44_complete_record_1th.txt','w')
#	f_write.write('34,138834')
#	f_write.close()
		

def mk_symmetry_num_44(first_XY):
	symmetry_dict_44 = {'12':1, '21':2, '34':3, '43':4}
	return symmetry_dict_44[first_XY]

def symmetrical_movement_XY_44(X,Y,symmetry_num):
	if symmetry == 1:
		return 5-Y, 5-X
	elif symmetry == 2:
		return 5-X, 5-Y
	elif symmetry == 3:
		return X, Y
	elif symmetry == 4:
		return Y, X
	else:
		return False

def symmetrical_movement_board(board,symmetry):
	new_board = np.zeros((BOARD_SIZE,BOARD_SIZE))
	for X in range(BOARD_SIZE):
		for Y in range(BOARD_SIZE):
			new_X, new_Y = symmetrical_movement_XY(X,Y,symmetry)
			new_board[new_X][new_Y] = deepcopy(board[X][Y])
	return new_board

def find_next_best_with_symmetry(board,lst_best,symmetry):
	new_board = symmetrical_movement_board(board,symmetry)
	#next_X, next_Y = find_next_best(new_board,lst_best)
	next_X, next_Y = symmetrical_movement_XY(next_X,next_Y,symmetry)
	return next_X, next_Y



if __name__ == '__main__':
	Board = Board()
	Board.play_2players_44()


