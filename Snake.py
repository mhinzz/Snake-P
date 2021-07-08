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
snakeLength	= 1
snakeSize	= 20
snakeSpeed	= 10
gameMenu	= True
gameStart	= True
gameOver	= False
messageFont	= pygame.font.SysFont('ubuntu', 35)
scoreFont	= pygame.font.SysFont('ubuntu', 25)
otherFont	= pygame.font.SysFont('ubuntu', 25)

class myMessage:
	def __init__(self, text, font, fontSize, colour):
		self.text= text
		self.font = font
		self.fontSize = fontSize
		self.colour = colour

def main():
	print("==================Starting game==================")
	gameMenuFunction(gameStart, gameOver, snakeLength)

def exit():
	print("==================Quiting Game==================")
	pygame.quit()
	quit()

def printScore(highScore, score):
	gameDisplay.blit(
		scoreFont.render(
			"High Score: " + str(highScore) + " Score: " + str(score), 
			True, 
			orange
		), 
		[0,5]
	)

def drawSnake(snakeSize, snakePixels):
	for pixel in snakePixels:
		pygame.draw.rect(gameDisplay, white, [pixel[0], pixel[1], snakeSize, snakeSize])

def runAction(xSpeed, ySpeed):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
		elif event.type == pygame.KEYDOWN:
			print(event)
			if event.key == pygame.K_LEFT and xSpeed == 0:
				xSpeed = -snakeSize
				ySpeed = 0
			elif event.key == pygame.K_RIGHT and xSpeed == 0:
				xSpeed = snakeSize
				ySpeed = 0
			elif event.key == pygame.K_UP and ySpeed == 0 :
				xSpeed = 0
				ySpeed = -snakeSize
			elif event.key == pygame.K_DOWN and ySpeed == 0:
				xSpeed = 0
				ySpeed = snakeSize
			elif event.key == pygame.K_SPACE:
				runGame(False)
			elif event.key == pygame.K_BACKSPACE:
				exit()
			else:
				continue
	return xSpeed, ySpeed

def gameMenuFunction(gameStart, gameOver, snakeLength):
	while True:
		gameDisplay.fill(black)
		pygame.draw.rect(gameDisplay, grey, [0, 0, width, 40])

		messages = [
			myMessage("Error", messageFont, 35, red),
			myMessage("High Score: " + str(snakeLength - 1), scoreFont, 25, orange),
			myMessage("Score: " + str(snakeLength - 1), scoreFont, 25, orange),
			myMessage("", scoreFont, 25, white),
			myMessage("Press 'Space' for new game,", scoreFont, 25, white),
			myMessage("and 'Backspace' to exit", scoreFont, 25, white),
			myMessage("", scoreFont, 25, white),
			myMessage("Use arrow keys to move", scoreFont, 25, white)
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

		# printScore(snakeLength - 1)
		pygame.display.update()

		runAction(0,0)

def runGame(gameOver):
	# Initial snake possition and speed 
	x = width / 2
	y = height / 2
	xSpeed = 0
	ySpeed = 0
	snakePixels = []
	snakeLength = 1

	# Set first food position
	foodX = round(random.randrange(0, width  - snakeSize) / 20.0) * 20.0
	foodY = round(random.randrange(30, height - snakeSize) / 20.0) * 20.0

	while not gameOver:
		xSpeed, ySpeed = runAction(xSpeed, ySpeed)
		
		# If snake goes out of play area go to game menu with game over 
		if (x >= width) or (x < 0) or (y >= height) or (y < 30):
			gameOver = True
			break

		# Consume food create new food if inside snake 
		if (x == foodX) and (y == foodY):
			foodX = round(random.randrange(0, width  - snakeSize) / 20.0) * 20.0
			foodY = round(random.randrange(30, height - snakeSize) / 20.0) * 20.0
			snakeLength += 1

		# Set the new speed
		x += xSpeed
		y += ySpeed

		# Clear screen and set food
		gameDisplay.fill(black)
		pygame.draw.rect(gameDisplay, grey, [0, 0, width, 40])
		pygame.draw.rect(gameDisplay, orange, [foodX, foodY, snakeSize, snakeSize])

		# Set new snake position
		snakePixels.append([x, y])
		if len(snakePixels) > snakeLength:
			del snakePixels[0]
		drawSnake(snakeSize, snakePixels)
		printScore(snakeLength - 1, snakeLength - 1)

		# If snake is inside itself go to menu with game over
		for pixel in snakePixels[:-1]:
			if pixel == [x, y]:
				gameOver = True
				break

		# Draw the updated food, score, and snake
		pygame.display.update()

		# Next game tick
		clock.tick(snakeSpeed)

	gameMenuFunction(False, gameOver, snakeLength)

if __name__ == "__main__":
	main()