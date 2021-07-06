import pygame
import time
import random

pygame.init()

# Define Colours 
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 165, 0)

width, height = 600, 600

gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption("mhinzz Snake Game")

clock = pygame.time.Clock()

gameOver = False
gameMenu = False

snakeSize = 10
snakeSpeed = 15

messageFont = pygame.font.SysFont('ubuntu', 30)
scoreFont   = pygame.font.SysFont('ubuntu', 25)

def printScore(score):
	text = scoreFont.render("Score: " + str(score), True, orange)
	gameDisplay.blit(text, [0,0])

def drawSnake(snakeSize, snakePixels):
	for pixel in snakePixels:
		pygame.draw.rect(gameDisplay, white, [pixel[0], pixel[1], snakeSize, snakeSize])

def runAction(event, xSpeed, ySpeed):
	if event.type == pygame.QUIT:
		gameOver = True
	if event.type == pygame.KEYDOWN:
		print(event)
		if event.key == pygame.K_LEFT:
			xSpeed = -snakeSize
			ySpeed = 0
		if event.key == pygame.K_RIGHT:
			xSpeed = snakeSize
			ySpeed = 0
		if event.key == pygame.K_UP:
			xSpeed = 0
			ySpeed = -snakeSize
		if event.key == pygame.K_DOWN:
			xSpeed = 0
			ySpeed = snakeSize
	return xSpeed, ySpeed

# def gameMenuFunction(gameOver, gameMenu, snakeLength):
def gameMenuFunction(snakeLength):
	while gameMenu:
		gameDisplay.fill(black)
		gameOverMessage = messageFont.render("Game Over!", True, red)
		gameDisplay.blit(gameOverMessage, [width / 3, height / 2])
		printScore(snakeLength - 1)
		pygame.display.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameOver = True
				gameMenu = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					gameOver = True
					gameMenu = False
				if event.key == pygame.K_2:
					runGame()
	return gameOver, gameMenu

def runGame():
	gameOver = False
	gameMenu = False

	x = width / 2
	y = height / 2

	xSpeed = 0
	ySpeed = 0

	snakePixels = []
	snakeLength = 1

	foodX = round(random.randrange(0, width  - snakeSize) / 10.0) * 10.0
	foodY = round(random.randrange(0, height - snakeSize) / 10.0) * 10.0

	while not gameOver:

		# gameOver, gameMenu = gameMenu(gameOver, gameMenu, snakeLength)
		gameMenuFunction(snakeLength)

		for event in pygame.event.get():
			xSpeed, ySpeed = runAction(event, xSpeed, ySpeed)
		
		if (x >= width) or (x < 0) or (y >= height) or (y < 0):
			gameMenu = True

		x += xSpeed
		y += ySpeed

		gameDisplay.fill(black)
		pygame.draw.rect(gameDisplay, orange, [foodX, foodY, snakeSize, snakeSize])

		snakePixels.append([x, y])

		if len(snakePixels) > snakeLength:
			del snakePixels[0]

		for pixel in snakePixels[:-1]:
			if pixel == [x, y]:
				gameMenu = True

		drawSnake(snakeSize, snakePixels)
		printScore(snakeLength - 1)

		pygame.display.update()

		if (x == foodX) and (y == foodY):
			foodX = round(random.randrange(0, width  - snakeSize) / 10.0) * 10.0
			foodY = round(random.randrange(0, height - snakeSize) / 10.0) * 10.0

			snakeLength += 1
		
		clock.tick(snakeSpeed)

	pygame.quit()
	quit()

runGame()
