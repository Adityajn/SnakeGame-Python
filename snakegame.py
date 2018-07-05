import curses
import time
import random
from threading import Thread
import sys

class GameBoard(object):
	def __init__(self,row,col,size=2):
		self.size = size
		self.col=col
		self.row=row

		self.finished = False

		#inititalize empty board
		self.board = [[" " for _ in range(col)] for _ in range(row)]
		
		#initialize snake positions
		head = (int(row/2),int(col/2))
		self.snake = [ ((head[0]+i),head[1]) for i in range(size) ]
		
		# put food
		self.food = [(10,20)]
		food = Thread(target=self.putFood)
		food.start()

		# 1- up, 2-right, 3-down, 4- left
		self.move = 4
		self.oldmove = 1

	def __str__(self):
		score = "Score : {}".format(str(len(self.snake)-2).zfill(2))
		board='='*(self.col-13)+" "+score+" ===\n"
		for r in range(self.row):
			curr = "="
			for c in range(self.col):
				curr += self.board[r][c]
			board += curr+"=\n"
		board+='='*(self.col+2)+"\n"
		return board
		

	def refreshBoard(self):
		self.board = [[" " for _ in range(self.col)] for _ in range(self.row)]
		if not self.changeSnake():
			self.finished = True
			return False
		snake = self.snake
		self.board[snake[0][0]][snake[0][1]] = "@"
		for tail in snake[1:]:
			self.board[tail[0]][tail[1]]="*"
		for food in self.food:
			self.board[food[0]][food[1]]="$"
		return True

	def changeSnake(self):
		tail = self.snake[-1]
		self.snake=self.snake[:-1]
		
		r = self.snake[0][0]
		c = self.snake[0][1]
		if self.move == 1:
			r -= 1
		elif self.move==2:
			c += 1
		elif self.move==3:
			r += 1
		else:
			c -= 1
		newhead = (r,c)
			
		if newhead in self.snake or newhead[0]<0 or newhead[0]>self.row-1 or newhead[1]<0 or newhead[1]>self.col-1:
			return False
		elif newhead in self.food:
			self.food.remove(newhead)
			self.snake = [newhead]+self.snake+[tail]
			return True
		else:
			self.snake = [newhead]+self.snake
			return True

	def putFood(self):
		"""
			randomly select a point which is not on snake and put food
		"""
		while True:
			r = int(random.random()*1000)%self.row
			c = int(random.random()*1000)%self.col
			if self.finished:
				break
			if (r,c) not in self.snake+self.food:
				self.food.append((r,c))
			time.sleep((random.random()*100)%6)

	def control(self,move):
		if not abs(self.move-move)==2:
			self.move=move

	def gameOver(self): 
		score = "Score : {}".format(str(len(self.snake)-2).zfill(2))
		board='='*(self.col-13)+" "+score+" ===\n"
		for r in range(self.row):
			curr = "="
			for c in range(self.col):
				curr += self.board[r][c]
			board += curr+"=\n"
		notify = '= Press \"n\" to start a new game or any key to Exit ='
		rowl = self.row-len(notify)
		board+='='*int(rowl/2) + notify + '='*int(rowl/2)
		return board

def initialize(window):
	board = GameBoard(20,50)
	game = True
	while game:
		window.clear()
		window.insstr(0, 0, str(board))
		window.refresh()
		status = True
		control = Thread(target=controller,args=(board,window))
		control.start()
		while status:
			window.clear()
			window.insstr(0, 0, str(board))
			window.refresh()
			speed = (10/(len(board.snake)+8))
			time.sleep(speed)
			status = board.refreshBoard()
		(game,board) = gameOver(window,board)

def gameOver(window,board):
	window.clear()
	window.insstr(0,0,str(board.gameOver()))
	window.refresh()
	ch= window.getch()
	if str(ch)==ord("n"):
		board = GameBoard(20,50)
		return (True,board)
	else:
		return (False,None)

def controller(board,window):
	while True:
		ch = window.getch()
		if ch==curses.KEY_UP:
			board.control(1)
		elif ch==curses.KEY_DOWN:
			board.control(3)
		elif ch==curses.KEY_LEFT:
			board.control(4)
		elif ch==curses.KEY_RIGHT:
			board.control(2)
		if board.finished:
			break

if __name__=='__main__':
	curses.wrapper(initialize)