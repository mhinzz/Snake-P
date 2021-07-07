import pygame
import time
import random

pygame.init()

# Define colours 
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 165, 0)

# Define display
width = 700
height = 600
gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption("mhinzz Snake Game")

# Initialize clock
clock = pygame.time.Clock()

# Initial parameters
snakeLength	= 1
snakeSize	= 10
snakeSpeed	= 15
gameMenu	= True
gameStart	= True
gameOver	= False
messageFont	= pygame.font.SysFont('ubuntu', 35)
scoreFont	= pygame.font.SysFont('ubuntu', 25)

def main():
	print("==================Starting game==================")
	gameMenuFunction(gameStart, gameOver, snakeLength)

def exit():
	print("==================Quiting Game==================")
	pygame.quit()
	quit()

def printScore(score):
	text = scoreFont.render("Score: " + str(score), True, orange)
	gameDisplay.blit(text, [0,0])

def drawSnake(snakeSize, snakePixels):
	for pixel in snakePixels:
		pygame.draw.rect(gameDisplay, white, [pixel[0], pixel[1], snakeSize, snakeSize])

def runAction(xSpeed, ySpeed):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
		elif event.type == pygame.KEYDOWN:
			print(event)
			if event.key == pygame.K_LEFT:
				xSpeed = -snakeSize
				ySpeed = 0
			elif event.key == pygame.K_RIGHT:
				xSpeed = snakeSize
				ySpeed = 0
			elif event.key == pygame.K_UP:
				xSpeed = 0
				ySpeed = -snakeSize
			elif event.key == pygame.K_DOWN:
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

		if gameStart:
			gameMessage = messageFont.render("Game Start!", True, red)
		elif gameOver:
			gameMessage = messageFont.render("Game Over!", True, red)
		else:
			gameMessage = messageFont.render("Error", True, red)

		gameDisplay.blit(gameMessage, 
			[
				(( width  / 2) - (gameMessage.get_width()  / 2)),
				(((height / 2) - (gameMessage.get_height() / 2)) - 35)
			]
		)

		highScore = scoreFont.render("High Score: " + str(snakeLength - 1), True, orange)
		gameDisplay.blit(highScore, 
			[
				(( width  / 2) - (highScore.get_width()  / 2)),
				(((height / 2) - (highScore.get_height() / 2)) - 0)
			]
		)
		score = scoreFont.render("Score: " + str(snakeLength - 1), True, orange)
		gameDisplay.blit(score, 
			[
				(( width  / 2) - (score.get_width()  / 2)),
				(((height / 2) - (score.get_height() / 2)) + 25)
			]
		)
		# gameMessage.len

		# printScore(snakeLength - 1)
		pygame.display.update()

		runAction(0,0)
		# for event in pygame.event.get():
		# 	if event.type == pygame.QUIT:
		# 		exit()
		# 	if event.type == pygame.KEYDOWN:
		# 		if event.key == pygame.K_1:
		# 			exit()
		# 		if event.key == pygame.K_2:
		# 			runGame(False)
		# 	else:
		# 		continue

def runGame(gameOver):
	# Initial snake possition and speed 
	x = width / 2
	y = height / 2
	xSpeed = 0
	ySpeed = 0
	snakePixels = []
	snakeLength = 1

	# Set first food position
	foodX = round(random.randrange(0, width  - snakeSize) / 10.0) * 10.0
	foodY = round(random.randrange(0, height - snakeSize) / 10.0) * 10.0

	while not gameOver:
		xSpeed, ySpeed = runAction(xSpeed, ySpeed)
		
		# If snake goes out of play area go to game menu with game over 
		if (x >= width) or (x < 0) or (y >= height) or (y < 0):
			gameOver = True
			break

		# Consume food create new food if inside snake 
		if (x == foodX) and (y == foodY):
			foodX = round(random.randrange(0, width  - snakeSize) / 10.0) * 10.0
			foodY = round(random.randrange(0, height - snakeSize) / 10.0) * 10.0
			snakeLength += 1

		# Set the new speed
		x += xSpeed
		y += ySpeed

		# Clear screen and set food
		gameDisplay.fill(black)
		pygame.draw.rect(gameDisplay, orange, [foodX, foodY, snakeSize, snakeSize])

		# Set new snake position
		snakePixels.append([x, y])
		if len(snakePixels) > snakeLength:
			del snakePixels[0]
		drawSnake(snakeSize, snakePixels)
		printScore(snakeLength - 1)

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