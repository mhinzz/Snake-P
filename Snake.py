import pygame
import time
import random

pygame.init()

# Define colours 
white = (255, 255, 255)
grey = (30, 30, 30)
black = (0, 0, 0)
orange = (255, 165, 0)
red = (255, 0, 0)

# Define display
width = 1000
height = 800
gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption("mhinzz Snake Game")

# Initialize clock
clock = pygame.time.Clock()

# Initial parameters
# length	= 1
# snakeSize	= 20
# speed	= 10
gameMenu	= True
gameStart	= True
gameOver	= False
messageFont	= pygame.font.SysFont('ubuntu', 35)
scoreFont	= pygame.font.SysFont('ubuntu', 25)
otherFont	= pygame.font.SysFont('ubuntu', 25)

class MyMessage:
	def __init__(self, text, font, fontSize, colour):
		self.text= text
		self.font = font
		self.fontSize = fontSize
		self.colour = colour

class Snake:
	size = 20
	speed = 10
	def __init__(self, x, y, xSpeed, ySpeed, pixels, length):
		self.x = x
		self.y = y
		self.xSpeed = xSpeed
		self.ySpeed = ySpeed
		self.pixels = pixels
		self.length = length

def main():
	print("==================Starting game==================")
	snk = Snake(width / 2, height / 2, 0, 0, [], 1)
	gameMenuFunction(gameStart, gameOver, snk)

def exit():
	print("==================Quiting Game==================")
	pygame.quit()
	quit()

def printScore(highScore, score):
	gameDisplay.blit(
		scoreFont.render(
			"High Score: " + str(highScore) + "    Score: " + str(score),
			True,
			orange
		), 
		[10,5]
	)

def drawSnake(snakeSize, pixels):
	for pixel in pixels:
		pygame.draw.rect(gameDisplay, white, [pixel[0], pixel[1], snakeSize, snakeSize])

def runAction(snk):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
		elif event.type == pygame.KEYDOWN:
			print(event)
			if event.key == pygame.K_LEFT and snk.xSpeed == 0:
				snk.xSpeed = -snk.size
				snk.ySpeed = 0
			elif event.key == pygame.K_RIGHT and snk.xSpeed == 0:
				snk.xSpeed = snk.size
				snk.ySpeed = 0
			elif event.key == pygame.K_UP and snk.ySpeed == 0 :
				snk.xSpeed = 0
				snk.ySpeed = -snk.size
			elif event.key == pygame.K_DOWN and snk.ySpeed == 0:
				snk.xSpeed = 0
				snk.ySpeed = snk.size
			elif event.key == pygame.K_SPACE:
				runGame(False, snk)
			elif event.key == pygame.K_BACKSPACE:
				exit()
			else:
				continue
	return snk

def gameMenuFunction(gameStart, gameOver, snk):
	while True:
		gameDisplay.fill(black)
		pygame.draw.rect(gameDisplay, grey, [0, 0, width, 40])

		messages = [
			MyMessage("Error", messageFont, 35, red),
			MyMessage("High Score: " + str(snk.length - 1), scoreFont, 25, orange),
			MyMessage("Score: " + str(snk.length - 1), scoreFont, 25, orange),
			MyMessage("", scoreFont, 25, white),
			MyMessage("Press 'Space' for new game,", scoreFont, 25, white),
			MyMessage("and 'Backspace' to exit", scoreFont, 25, white),
			MyMessage("", scoreFont, 25, white),
			MyMessage("Use arrow keys to move", scoreFont, 25, white)
		]

		if gameStart:
			messages[0].text = "Game Start!"
		elif gameOver:
			messages[0].text = "Game Over!"

		start = 80
		for message in messages:
			text = message.font.render(message.text, True, message.colour)
			gameDisplay.blit(text, 
				[
					(( width  / 2) - (text.get_width()  / 2)),
					(((height / 2) - (text.get_height() / 2)) - start)
				]
			)
			start -= message.fontSize

		# printScore(length - 1)
		pygame.display.update()

		runAction(snk)

def runGame(gameOver, snk):
	# Initial snake possition and speed 
	
	# x = width / 2
	# y = height / 2
	# xSpeed = 0
	# ySpeed = 0
	# pixels = []
	# length = 1

	# Set first food position
	foodX = round(random.randrange(0, width  - snk.size) / 20.0) * 20.0
	foodY = round(random.randrange(30, height - snk.size) / 20.0) * 20.0

	while not gameOver:
		snk = runAction(snk)
		
		# If snake goes out of play area go to game menu with game over 
		if (snk.x >= width) or (snk.x < 0) or (snk.y >= height) or (snk.y < 30):
			gameOver = True
			break

		# Consume food create new food if inside snake 
		if (snk.x == foodX) and (snk.y == foodY):
			while True:
				foodX = round(random.randrange(0,  width  - snk.size) / 20.0) * 20.0
				foodY = round(random.randrange(30, height - snk.size) / 20.0) * 20.0
				if not [foodX, foodY] in snk.pixels:
					break
			snk.length += 1

		# Set the new speed
		snk.x += snk.xSpeed
		snk.y += snk.ySpeed

		# Clear screen and set food
		gameDisplay.fill(black)
		pygame.draw.rect(gameDisplay, grey, [0, 0, width, 40])
		pygame.draw.rect(gameDisplay, orange, [foodX, foodY, snk.size, snk.size])

		# Set new snake position
		snk.pixels.append([snk.x, snk.y])
		if len(snk.pixels) > snk.length:
			del snk.pixels[0]
		drawSnake(snk.size, snk.pixels)
		printScore(snk.length - 1, snk.length - 1)

		# If snake is inside itself go to menu with game over
		for pixel in snk.pixels[:-1]:
			if pixel == [snk.x, snk.y]:
				gameOver = True
				break

		# Draw the updated food, score, and snake
		pygame.display.update()

		# Next game tick
		clock.tick(snk.speed)

	gameMenuFunction(False, gameOver, snk)

if __name__ == "__main__":
	main()