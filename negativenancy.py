#!/usr/bin/python

from curses import initscr,curs_set,newwin,endwin,KEY_RIGHT,KEY_LEFT,KEY_DOWN
from random import randrange
from sys import exit

initscr()
curs_set(0)
window = newwin(30,30,0,0)
window.keypad(1)
# window.nodelay(1)
window.border('|','|','-','-','+','+','+','+')
key=KEY_RIGHT
window.timeout(70)
x = 14
score = 0

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

def introMessage():
	window.addstr(28, x, ':D')
	for line in INTRO_MESSAGE:
		window.addstr(line[0],line[1],line[2])
	for line in INTRO_ARROW:
		window.addstr(line[0],line[1],line[2])

def clearIntroMessage():
	for line in INTRO_MESSAGE:
		window.hline(line[0],line[1],' ',len(line[2]))
	for line in INTRO_ARROW:
		window.hline(line[0],line[1],' ',len(line[2]))

class NegativeNancy():
	def __init__(self):
		self.length = randrange(5,15,1)
		self.x = randrange(2,28-self.length,1)
		
def moveCharacter(key, x):
	if key==KEY_LEFT:
		if x - 1 > 0:
			window.addstr(28,x+1,' ',2)
			x -= 1
		else: pass
	elif key==KEY_RIGHT:
		if x + 1 < 28:
			window.addstr(28,x,' ',2)
			x += 1
		else: pass
	else: pass
	return x
	
def exitMessage(score):
	window.erase()
	window.addstr(28,10,"X______X")
	window.addstr(10,3,"You just dodged")
	if score == 1:
		window.addstr(11,3,"1 Negative Nancy!")
	else:
		window.addstr(11,3,"%d Negative Nancys!" % score)
	window.addstr(13, 3, "Press DOWN to finish.")

try:
	introMessage()
	while True:
		key = window.getch()
		if key == KEY_DOWN:
			break
	clearIntroMessage()
	while key != 27:	# as far as I know, 27 is random
		window.addstr(0, 3, ' Score: '+str(score)+' ')
		nn = NegativeNancy()
		for y in range(1, 29):
			if y > 1:
				window.hline(y - 1, nn.x-1, ' ', nn.length+2)
			window.hline(y, nn.x, '_', nn.length)
			window.addch(y, nn.x-1, '-')
			window.addch(y, nn.x+nn.length, '-')
			key = window.getch()
			x = moveCharacter(key, x)
			window.addstr(28, x, ':D')
		if x >= nn.x-2 and x <= nn.x+nn.length:
			break
		window.hline(28, nn.x-1, ' ', nn.length+2)
		score += 1
finally: 
	exitMessage(score)
	while True:
		key = window.getch()
		if key == KEY_DOWN:
			endwin()
			exit()