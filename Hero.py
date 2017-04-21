import pygame,os,sys
import Globals

class Hero():
	def __init__ (self):
		self.x = 0
		self.y = 0
		self.velX = 0
		self.velY = 0
		self.speed = Globals.playerSpeed
		self.state = 1
		self.nearestRow = 0
		self.nearestCol = 0
		self.homeX = 0
		self.homeY = 0
		self.anim = 1
		self.anim_pacmanL = {}
		self.anim_pacmanR = {}
		self.anim_pacmanU = {}
		self.anim_pacmanD = {}
		self.anim_pacmanS = {}
		self.anim_pacmanCurrent = {}
		for i in range(1, 5, 1):
			self.anim_pacmanL[i] = pygame.image.load("res/sprite/"+Globals.selectedCharacter+"c-l " + str(i) + ".png").convert_alpha()
			self.anim_pacmanR[i] = pygame.image.load("res/sprite/"+Globals.selectedCharacter+"c-r " + str(i) + ".png").convert_alpha()
			self.anim_pacmanU[i] = pygame.image.load("res/sprite/"+Globals.selectedCharacter+"c-u " + str(i) + ".png").convert_alpha()
			self.anim_pacmanD[i] = pygame.image.load("res/sprite/"+Globals.selectedCharacter+"c-d " + str(i) + ".png").convert_alpha()
			self.anim_pacmanS[i] = self.anim_pacmanR[1]
		self.pelletSndNum = 0
		
	def Move (self):
		self.nearestRow = int(self.y / 25)
		self.nearestCol = int(self.x / 25)
		if not Globals.thisLevel.CheckIfHitWall((self.x + self.velX, self.y + self.velY), (56,99)):
			self.x += self.velX
			self.y += self.velY
		else:
			self.velX = 0
			self.velY = 0
			
	def Draw (self):
		if Globals.thisGame.mode == 3:
			return False
		if self.velX > 0:
			self.anim_pacmanCurrent = self.anim_pacmanR
		elif self.velX < 0:
			self.anim_pacmanCurrent = self.anim_pacmanL
		elif self.velY > 0:
			self.anim_pacmanCurrent = self.anim_pacmanD
		elif self.velY < 0:
			self.anim_pacmanCurrent = self.anim_pacmanU
		Globals.screen.blit (self.anim_pacmanCurrent[ self.animFrame ], (self.x - Globals.thisGame.screenPixelPos[0], self.y - Globals.thisGame.screenPixelPos[1]))
		if Globals.thisGame.mode == 1:
			if not self.velX == 0 or not self.velY == 0:
				self.anim += 1
			if self.anim == 6:
				self.animFrame += 1
				self.anim = 1
			if self.animFrame == 5:
				self.animFrame = 1