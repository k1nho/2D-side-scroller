import pygame
import os
import sys
import math
import random
from pygame.locals import *


# initialize pygame and window size

pygame.init()
WIDTH = 800
HEIGHT = 477
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# set caption
pygame.display.set_caption('2D side scroller')

# set background 
background = pygame.image.load(os.path.join('images', 'bg.png')).convert()
background_x = 0
background_y = background.get_width()

# set clock
clock = pygame.time.Clock()


class Player(object):

	# set different animation frames
	# 1) running motion
	run = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(8,16)]
	# 2) jumping motion
	jump = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(1,8)]
	# 3) sliding motion (mantain 5 frames of motion when sliding)
	slide = [pygame.image.load(os.path.join('images', 'S1.png')),pygame.image.load(os.path.join('images', 'S2.png')),pygame.image.load(os.path.join('images', 'S2.png')),
	pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),pygame.image.load(os.path.join('images', 'S2.png')), 
	pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S3.png')),
	pygame.image.load(os.path.join('images', 'S4.png')), pygame.image.load(os.path.join('images', 'S5.png'))]
	# 4) collision motion
	fall = pygame.image.load(os.path.join('images', '0.png'))
	jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]

	# constructor
	def __init__(self, x , y , width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.jumping = False
		self.sliding = False
		self.collision = False
		self.jump_count = False
		self.slide_count = False
		self.run_count = False
		self.slide_up = False

	# member function to draw the character
	def draw_char(self, WIN):

		if self.collision:
			WIN.blit(self.fall, (self.x, self.y+30))

		# if character is jumping
		elif self.jumping:
			self.y -= self.jumpList[self.jump_count] * 1.2
			WIN.blit(self.jump[self.jump_count // 18], (self.x, self.y))
			self.jump_count += 1

			# check if we have our jump count has terminated
			if self.jump_count > 108:
				self.jump_count = 0
				self.jumping = False
				self.run_count = 0
			# create hitbox for character when jumping
			self.hitbox = (self.x + 4, self.y, self.width - 24, self.height -10)
		# if character is sliding
		elif self.sliding or self.slide_up:
			if self.slide_count < 20:
				self.y += 1
			elif self.slide_count == 80:
				self.y -= 19
				self.sliding = False
				self.slideUp = True
			elif self.slide_count >20 and self.slide_count < 80:
				# create hitbox for character when sliding
				self.hitbox = (self.x, self.y +3, self.width -8, self.height -35)

			if self.slide_count >= 110:
				self.slide_count = 0
				self.slide_up = False
				self.runCount = 0
				# create hitbox for character when sliding
				self.hitbox = (self.x +4, self.y, self.width-24, self.height -10)
            # draw the correct animation onto the surface
			WIN.blit(self.slide[self.slide_count // 10], (self.x, self.y))
			self.slide_count += 1

		# default: running
		else:
			if self.run_count > 42:
				self.run_count = 0
			# draw the correct animation onto the surface
			WIN.blit(self.run[self.run_count // 6], (self.x, self.y))
			self.run_count += 1
			self.hitbox = (self.x +4, self.y, self.width -24, self.height -13)

		#draw player hitbox
		pygame.draw.rect(WIN, (255,0,0), self.hitbox, 2)

class Saw(object):

	# set animation
	rotate = [pygame.image.load(os.path.join('images', 'SAW0.PNG')),pygame.image.load(os.path.join('images', 'SAW1.PNG')),
	pygame.image.load(os.path.join('images', 'SAW2.PNG')),pygame.image.load(os.path.join('images', 'SAW3.PNG'))]

	def __init__(self,x,y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.rotate_count = 0
		self.vel =1.4

	def draw_obstacle(self,WIN):
		self.hitbox = (self.x +10, self.y +5, self.width -20, self.height - 5)
		pygame.draw.rect(WIN,(255,0,0), self.hitbox, 2)

		# animation for the saw
		if self.rotate_count >=8:
			self.rotate_count = 0
		# scale the image to 64x64 before drawing
		WIN.blit(pygame.transform.scale(self.rotate[self.rotate_count //2], (64,64)), (self.x, self.y))
		self.rotate_count += 1

	def collision(self,rect):
		if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
			if rect[1] + rect[3] > self.hitbox[1]:
				return True
		return False


#inherit from the saw class
class Spike(Saw):
	img = pygame.image.load(os.path.join('images', 'spike.png'))

	def draw_obstacle(self, WIN):
		self.hitbox = (self.x +10, self.y, 28, 315)
		pygame.draw.rect(WIN, (255,0,0), self.hitbox, 2)
		WIN.blit(self.img , (self.x, self.y))

	def collision(self,rect):
		if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
			if rect[1] + rect[3] > self.hitbox[1]:
				return True
		return False


def win_redraw(character):
	WIN.blit(background, (background_x, 0))
	WIN.blit(background, (background_y, 0))
	character.draw_char(WIN)

	# search every obstacle and draw one by one into the window
	for obstacle in obstacles:
		obstacle.draw_obstacle(WIN)

	pygame.display.update()




run = True
framerate = 30
pygame.time.set_timer(USEREVENT+1, 500)
pygame.time.set_timer(USEREVENT+2, random.randrange(2000, 3500))
character = Player(200, 313,64,64)
obstacles = []

# create game loop
while run:
	win_redraw(character)
	clock.tick(framerate)
	keys = pygame.key.get_pressed()

	# move background image
	background_x -= 1.4
	background_y -= 1.4

	# if our background reaches the maximum width, reset the background
	if background_x < background.get_width() * -1:
		background_x = background.get_width()

	if background_y < background.get_width() * -1:
		background_y = background.get_width()

	# check the keys pressed
	if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
		if not(character.jumping):
			character.jumping = True

	if keys[pygame.K_DOWN]:
		if not(character.sliding):
			character.sliding = True

	for obstacle in obstacles:
		obstacle.x -= 1.4
		if obstacle.collision(character.hitbox):
			character.collision = True
		if obstacle.x < obstacle.width *-1:
			obstacles.pop(obstacles.index(obstacle))

	for event in pygame.event.get():
		# quit the game
		if event.type == pygame.QUIT:
			run = False
			pygame.quit()
			quit()
		# increase the framerate
		if event.type == USEREVENT+1:
			framerate +=1

		if event.type == USEREVENT+2:
			select_object = random.randrange(0,2)
			# determine which type of obstacle to append to the obstacle list
			if select_object == 0:
				obstacles.append(Saw(810,310,64,64))
			elif select_object == 1:
				obstacles.append(Spike(810,0,48,310))

	clock.tick(framerate)



