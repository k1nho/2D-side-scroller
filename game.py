import pygame
import os
import sys
import math
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
		self.jump_count = False
		self.slide_count = False
		self.run_count = False
		self.slide_up = False

	# member function to draw the character
	def draw_char(self, WIN):

		# if character is jumping
		if self.jumping:
			self.y -= self.jumpList[self.jump_count] * 1.2
			WIN.blit(self.jump[self.jump_count // 18], (self.x, self.y))
			self.jump_count += 1

			# check if we have our jump count has terminated
			if jump_count > 108:
				self.jump_count = 0
				self.jumping = False
				self.run_count = 0
		# if character is sliding
		elif self.sliding or self.slide_up:

		    if self.slide_count < 20:
                self.y += 1
            elif self.slide_count == 80:
                self.y -= 19
                self.sliding = False
                self.slideUp = True
            if self.slideCount >= 110:
                self.slideCount = 0
                self.slideUp = False
                self.runCount = 0
            # draw the correct animation onto the surface
           	WIN.blit(self.slide[slide_count // 10], (self.x, self.y))
           	self.slide_count += 1

		# default: running
		else:
			if self.run_count > 42:
				self.run_count = 0
			# draw the correct animation onto the surface
			WIN.blit(self.run[run_count // 6], (self.x, self.y))
			self.run_count += 1





