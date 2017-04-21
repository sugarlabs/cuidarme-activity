#! /usr/bin/python
# -*- coding: utf-8 -*-

import pygame, sys, os
import random

levelBoot = 0
tileIDName = {} # gives tile name (when the ID# is known)
tileID = {} # gives tile ID (when the name is known)
tileIDImage = {} # gives tile image (when the ID# is known)
screen = None
thisGame = None
thisLevel = None
player = None
dificulty = 2
ghostSpeed = 15
playerSpeed = 15
img_Background = None
itemTypes = ['star','star2','prop1','prop2','prop3','prop4','prop5','prop6']
itemsActivated = 1
snd_item = None
snd_timeOver = None
snd_good = None
snd_clock = None
snd_music = None
snd_win = None
maxTime = ''
dialog = 0
answer = 0
moverse = True
friendl = None
selectedCharacter = 'm'
questionId = 0
timer = 0
emotion = ''
actualMusic = ''

ghosts = {}
questionnum = 0
emotionnum = 0

INFO_ROOT_USER_ID = None
INFO_USERNAME = None
INFO_PASSWORD = None
INFO_LEAF_USER_ID = None
INFO_START_TIME = None
INFO_FINISH_TIME = None
INFO_STARS = 0

def GetCrossRef ():
	f = open("res/crossref.txt", 'r')
	lineNum = 0
	useLine = False
	for i in f.readlines():
		while len(i)>0 and (i[-1]=='\n' or i[-1]=='\r'): i=i[:-1]
		while len(i)>0 and (i[0]=='\n' or i[0]=='\r'): i=i[1:]
		str_splitBySpace = i.split(' ')
		j = str_splitBySpace[0]
		if (j == "'" or j == "" or j == "#"):
			useLine = False
		else:
			useLine = True
		if useLine == True:
			tileIDName[ int(str_splitBySpace[0]) ] = str_splitBySpace[1]
			tileID[ str_splitBySpace[1] ] = int(str_splitBySpace[0])
			thisID = int(str_splitBySpace[0])
			tileIDImage[ thisID ] = pygame.image.load("res/tiles/" + str_splitBySpace[1] + ".png")
			# else:
				# tileIDImage[ thisID ] = pygame.Surface((25,25))
		lineNum += 1

def getMaxTime():
	return int(maxTime)

