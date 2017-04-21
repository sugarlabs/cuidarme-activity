#! /usr/bin/python
# -*- coding: utf-8 -*-

import pygame,os,sys
import Globals
import data
import random

class game ():

	def __init__ (self):
		self.levelNum = 0
		self.score = 0

		self.mode = 0
		self.modeTimer = 0
		
		self.SetMode(3)
		
		# camera variables
		self.screenPixelPos = (0, 0) # absolute x,y position of the screen from the upper-left corner of the level
		self.screenNearestTilePos = (0, 0) # nearest-tile position of the screen from the UL corner
		self.screenPixelOffset = (0, 0) # offset in pixels of the screen from its nearest-tile position
		
		self.tilesX = 48
		self.tilesY = 33
		self.screenTileSize = (25, 25)
		self.screenSize = (self.screenTileSize[1] * self.tilesX, self.screenTileSize[0] * self.tilesY)

	def StartNewGame (self,level):
		self.levelNum = level
		#self.levelNum = 6
		self.score = 0
		self.screenPixelPos = (0, 0)
		self.screenNearestTilePos = (0, 0)
		self.screenPixelOffset = (0, 0)
		self.SetMode( 1 )
		Globals.thisLevel.LoadLevel( self.levelNum )

	def AddToScore (self, amount):
		self.score += amount
		Globals.INFO_STARS += amount
		
	def SmartMoveScreen (self):
		if (Globals.thisLevel.levelSize > 1200):
			possibleScreenX = Globals.player.x - ((self.screenTileSize[1] / 2) * self.tilesX)
			possibleScreenY = Globals.player.y - ((self.screenTileSize[0] / 2) * self.tilesY)
			# possibleScreenY = 0
			
			if possibleScreenX < 0:
				possibleScreenX = 0
			elif possibleScreenX > Globals.thisLevel.levelOffset:
				possibleScreenX = Globals.thisLevel.levelOffset
			if possibleScreenY < 0:
				possibleScreenY = 0
			elif possibleScreenY > Globals.thisLevel.heightOffset:
				possibleScreenY = Globals.thisLevel.heightOffset
			
			self.MoveScreen( (possibleScreenX, possibleScreenY) )
		
	def MoveScreen (self, (newX, newY) ):
		self.screenPixelPos = (newX, newY)
		self.screenNearestTilePos = (int(newY / 25), int(newX / 25)) # nearest-tile position of the screen from the UL corner
		self.screenPixelOffset = (newX - self.screenNearestTilePos[1]*25, newY - self.screenNearestTilePos[0]*25)
		
	def GetScreenPos (self):
		return self.screenPixelPos
		
	def GetLevelNum (self):
		return self.levelNum
	
	def changeToLevel(self,level):
		self.levelNum = level
		# Globals.INFO_STARS += self.score
		self.score = 0
		self.SetMode( 1 )
		Globals.thisLevel.LoadLevel( level )
		Globals.player.anim_pacmanCurrent = Globals.player.anim_pacmanS

	def SetNextLevel (self):
		self.levelNum =  random.randint(1,10)
		
		self.SetMode( 1 )
		Globals.INFO_STARS += self.score
		self.score = 0
		Globals.thisLevel.LoadLevel( self.GetLevelNum() )
		
		Globals.player.velX = 0
		Globals.player.velY = 0
		Globals.player.anim_pacmanCurrent = Globals.player.anim_pacmanS
		
	def SetMode (self, newMode):
		self.mode = newMode
		self.modeTimer = 0
		print " ***** GAME MODE IS NOW ***** " + str(newMode)