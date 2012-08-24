#!/usr/bin/python
from curses import initscr,curs_set,newwin,endwin,KEY_RIGHT,KEY_LEFT,KEY_DOWN
from random import randrange
import inspect
from sys import exit

FILE_NAME = inspect.getfile( inspect.currentframe() )
SCREEN_HEIGHT, SCREEN_WIDTH = 30, 30
GAME_HEIGHT, GAME_WIDTH = SCREEN_HEIGHT - 2, SCREEN_WIDTH - 2
DUDE = ':D'
INTRO_MESSAGE = [
	(7,3,"You're the smiley at"),
	(8,3,"the bottom of the screen."),
	(10,3,"Dodge the Negative Nancies"),
	(11,3,"with LEFT and RIGHT."),
	(13,3,"Press DOWN to continue."),
]
INTRO_ARROW = [
	(19,13," || "),
	(20,13," || "),
	(21,13," || "),
	(22,13," || "),
	(23,13," || "),
	(24,13," || "),
	(25,13,"\  /"),
	(26,13," \/ "),
]

# initialize global 'window' object
initscr()
curs_set(0)
window = newwin(SCREEN_HEIGHT,SCREEN_WIDTH,0,0)
window.keypad(1)
window.border('|','|','-','-','+','+','+','+')
key=KEY_RIGHT
window.timeout(70)

class NegativeNancy():
	def __init__(self):
		self.length = randrange(5,15,1)
		self.x = randrange(2,28-self.length,1)
	def placeNN(self, y):
		window.hline(y - 1, self.x - 1, ' ', self.length + len(DUDE))
	def printNN(self, y):
		window.hline(y, self.x, '_', self.length)
		window.addch(y, self.x - 1, '-')
		window.addch(y, self.x + self.length, '-')
	def erase(self):
		window.hline(GAME_HEIGHT, self.x - 1, ' ', self.length + 2)
		
class Game():
	def __init__(self):
		self.x = 14
		self.score = 0
	
	def printScoreline(self):
		window.addstr(0, 3, " Score: " + str(self.score) + " ")

	def printIntroMessage(self):
		while True:
			window.addstr(GAME_HEIGHT, self.x, DUDE)
			for line in INTRO_MESSAGE:
				window.addstr(line[0],line[1],line[2])
			for line in INTRO_ARROW:
				window.addstr(line[0],line[1],line[2])
			key = window.getch()
			if key == KEY_DOWN:
				return

	def eraseIntroMessage(self):
		for line in INTRO_MESSAGE:
			window.hline(line[0],line[1],' ',len(line[2]))
		for line in INTRO_ARROW:
			window.hline(line[0],line[1],' ',len(line[2]))

	def moveCharacter(self):
		key = window.getch()
		if key==KEY_LEFT:
			if self.x - 1 > 0:
				window.addstr(GAME_HEIGHT,self.x+1,' ',2)
				self.x -= 1
			else: pass
		elif key==KEY_RIGHT:
			if self.x + 1 < 28:
				window.addstr(GAME_HEIGHT,self.x,' ',2)
				self.x += 1
			else: pass
		window.addstr(GAME_HEIGHT, self.x, DUDE)
	
	def playGame(self):
		while True:
			self.printScoreline()
			nn = NegativeNancy()
			for y in range(1, GAME_HEIGHT + 1):
				if y > 1:
					nn.placeNN(y)
				nn.printNN(y)
				self.moveCharacter()
			if nn.x-len(DUDE) <= self.x <= nn.x + nn.length:
				return
			nn.erase()
			self.score += 1

	def printExitMessage(self):
		window.erase()
		window.addstr(GAME_HEIGHT,10,"X______X")
		window.addstr(10,3,"You just dodged")
		if self.score == 1:
			window.addstr(11,3,"1 Negative Nancy!")
		else:
			window.addstr(11,3,"%d Negative Nancys!" % self.score)
		window.addstr(13, 3, "Press DOWN to finish.")
		while True:
			key = window.getch()
			if key == KEY_DOWN:
				endwin()
				exit()

	def play(self):
		self.printIntroMessage()
		self.eraseIntroMessage()
		self.playGame()
		self.printExitMessage()

if __name__ == "__main__":
	game = Game()
	game.play()
