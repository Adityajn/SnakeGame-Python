import curses
import time
import random
from threading import Thread

class GameBoard(object):
	def __init__(self,row,col,size=2):
		self.size = size
		self.col=col
		self.row=row
		self.board = [[" " for _ in range(col)] for _ in range(row)]
		head = (int(row/2),int(col/2))
		self.snake = [ ((head[0]+i),head[1]) for i in range(size) ]
		
		# put food
		self.food = []
		food = Thread(target=self.putFood)
		food.start()

		# 1- up, 2-right, 3-down, 4- left 0-straight
		self.move = 4


	def showBoard(self):
		board='='*(self.col+2)+"\n"
		for r in range(self.row):
			curr = "="
			for c in range(self.col):
				curr += self.board[r][c]
			board += curr+"=\n"
		board+='='*(self.col+2)+"\n"
		print(board)
		

	def refreshBoard(self):
		self.board = [[" " for _ in range(self.col)] for _ in range(self.row)]
		if not self.changeSnake():
			return False
		snake = self.snake
		self.board[snake[0][0]][snake[0][1]] = "@"
		for tail in snake[1:]:
			self.board[tail[0]][tail[1]]="*"
		for food in self.food:
			self.board[food[0]][food[1]]="$"
		return True

	def changeSnake(self):
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
			if (r,c) not in self.snake+self.food:
				self.food.append((r,c))
			time.sleep(4)


if __name__ == "__main__":
	gb = GameBoard(20,50)
	status = True
	while status:
		gb.showBoard()
		status = gb.refreshBoard()
		time.sleep(.5)
	print("Game Over")
