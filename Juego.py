# -*- coding: utf-8 -*-

import pygame, sys, os, random
import Globals
import data
from Hero import Hero
from game import game
from pygame.locals import *
from itertools import chain
from threading import Timer
from copy import deepcopy
import olpcgames
import datetime
import urllib
import threading
#import gc
#gc.enable()

class Juego():

	def __init__ (self):
		self.clockTimer = 0
		pygame.init()
		pygame.font.init()
		self.clock = pygame.time.Clock()
		self.noticeTimer = 0
		self.showWinPopup = 0
		self.winPopupTimer = 0
		self.dialog = 0
		self.PUtimer = 0
		self.ghostDying = 0
		self.dyingPos = (0,0)
		self.ghostDieFrame = 1
		self.ghostAnimTimer = 1
		self.tryAgain = 0
		self.tryAgainTimer = 0
		self.timeOver = 0
		self.currentScreen = None
		self.emotionsTrivia = 1
		self.emotionSelected = 1
		self.screenToGo = 0
		self.persistenceChecked = 0
		self.illustrated = (0,0)

		# Control
		self.__dataProcessDefined = False
		self.__dataSentDefined = False
		
		self.__sendBatchThread = None
		self.__sendBatchInProgress = False

		self.window = pygame.display.set_mode((1200, 825),0,0)
		pygame.display.set_caption("Cuidarme")

		Globals.screen = pygame.display.get_surface()
		Globals.img_Background = pygame.image.load("res/backgrounds/Splash_1.png").convert()

		pygame.mixer.init()

		Globals.snd_item = pygame.mixer.Sound("res/sounds/FX/recojeitem2.ogg")
		Globals.snd_timeOver = pygame.mixer.Sound("res/sounds/FX/fanfarria_error.ogg")
		Globals.snd_good = pygame.mixer.Sound("res/sounds/FX/saleitem.ogg")
		self.explosion = pygame.mixer.Sound("res/sounds/FX/explosion.ogg")
		self.errorSound = pygame.mixer.Sound("res/sounds/FX/error.ogg")
		pygame.mixer.music.load('res/sounds/Musica/splash.ogg')
		
		self.btn_a1 = pygame.image.load("res/sprite/AnswerA_Off.png").convert_alpha()
		self.btn_b1 = pygame.image.load("res/sprite/AnswerB_Off.png").convert_alpha()
		self.btn_c1 = pygame.image.load("res/sprite/AnswerC_Off.png").convert_alpha()
		# self.__backgroundTransparent = pygame.image.load("res/backgrounds/0.png").convert()
		self.backgroundQuestion = pygame.image.load("res/backgrounds/Question.png").convert_alpha()
		self.ghostNormalFrame = pygame.image.load("res/sprite/ghost2.png").convert_alpha()
		self.ghostVulnerableFrame = pygame.image.load("res/sprite/ghost2_v.png").convert_alpha()
		self.clockBack = pygame.image.load("res/sprite/clockBack.png").convert_alpha()
		self.clockImg = pygame.image.load("res/sprite/ClockBig.png").convert_alpha()
		#self.timeOverImg = pygame.image.load("res/sprite/timeOver.png").convert_alpha()
		self.tryAgainImg = pygame.image.load("res/sprite/MessageTryAgain.png").convert_alpha()
		#self.winImg = pygame.image.load("res/sprite/mensaje_felicidades.png").convert_alpha()
		#self.popup = pygame.image.load("res/backgrounds/fondo_caritas.png").convert_alpha()
		self.buttonUp = pygame.image.load("res/sprite/boton_normal.png").convert_alpha()
		self.buttonDown = pygame.image.load("res/sprite/boton_presionado.png").convert_alpha()
		self.buttonstate = self.buttonUp
		self.fondoItem = pygame.image.load("res/sprite/fondoItem.png").convert_alpha()
		self.starIndicator = pygame.image.load("res/tiles/star2.png").convert_alpha()
		self.input_CloseGame_On = pygame.image.load("res/screens/CloseGame_On.png").convert_alpha()

		self.inst1 = pygame.image.load("res/sprite/cambiar.png").convert_alpha()
		self.inst2 = pygame.image.load("res/sprite/seleccionar.png").convert_alpha()

		self.__collectedItemsIndicator = Text(None, 30, 'x 0', (255, 255, 255), 55, 5)
		self.__timeRemainingIndicator = Text(None, 30, '5:00', (255, 255, 255), 610, 5)
		self.instructions = Text(None,15, 'Selecciona la emoción que', (255, 0, 255), 105, 160)
		self.instructions1 = Text(None,15, 'coincida con la descripción', (255, 0, 255), 105, 200)

	def checkPersistence(self):
		persistedRootUserId = None
		persistedUsername = None
		persistedPassword = None
		
		try:
			openedFile = None
			
			# Abrimos el archivo en modo Solo Lectura
			if olpcgames.ACTIVITY:  # Running as Activity
				name = os.getcwd() + '/UserInfo.txt'
				openedFile = open(name, 'r')
			else:
				openedFile = open('UserInfo.txt', 'r')
				
			# Recorremos el archivo linea por linea
			for lineIndex in enumerate(openedFile):
				
				# Primera linea: Root User Id
				if lineIndex[0] == 0:
					
					# Obtenemos el contenido de la linea correspondiente
					lineContent = lineIndex[1]
					
					# Extraemos el nombre de usuario de la linea leida (removemos tambien el salto de linea al final)
					persistedRootUserId = lineContent[11:len(lineContent) - 1]
										
				# Segunda linea: Username
				if lineIndex[0] == 1:
					
					# Obtenemos el contenido de la linea correspondiente
					lineContent = lineIndex[1]
					
					# Extraemos el nombre de usuario de la linea leida (removemos tambien el salto de linea al final)
					persistedUsername = lineContent[9:len(lineContent) - 1]
					
				# Tercera linea: Password
				if lineIndex[0] == 2:
					
					# Obtenemos el contenido de la linea correspondiente
					lineContent = lineIndex[1]
					
					# Extraemos el password de la linea leida
					persistedPassword = lineContent[9:len(lineContent) - 1]
					
					# Finalizamos el recorrido del archivo
					break
				
		except:
			persistedRootUserId = None
			persistedUsername = None
			persistedPassword = None
			
		finally:
			# Se cierra el archivo, sin importar lo que haya pasado
			try:
				openedFile.close
			except:
				pass

		# # Verificamos que los datos persistidos hayan sido leidos correctamente
		if (persistedRootUserId == None) or (persistedRootUserId == "") or (persistedUsername == None) or (persistedUsername == "") or (persistedPassword == None) or (persistedPassword == ""):
			# Pantalla para la creacion del archivo de persistencia
			# self.showScreen(5)
			self.persistenceChecked = 1
			self.screenToGo = 5
			
		else:
		# 	# Guardamos los datos obtenidos del archivo
			Globals.INFO_ROOT_USER_ID = persistedRootUserId
			Globals.INFO_USERNAME = persistedUsername
			Globals.INFO_PASSWORD = persistedPassword
			
			# Mostramos la pantalla de Login
			self.persistenceChecked = 1
			self.screenToGo = 4

	def savePersistence(self):
		if self.__dataProcessDefined == False:

			# Obtenemos la hora de finalizacion de la sesion de juego
			Globals.INFO_FINISH_TIME = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
			
			try:
				# Almacenamos la informacion de la sesion de juego recien finalizada
				openedFile = None
				
				# Creamos un archivo
				if olpcgames.ACTIVITY:  # Running as Activity
					name = os.getcwd() + '/UserInfo.txt'
					openedFile = open(name, 'a')
				else:
					openedFile = open('UserInfo.txt', 'a')
					
				# Escibimos el contenido apropiado
				openedFile.write('''---------------\n''')
				openedFile.write('''leafUserId:''' + str(Globals.INFO_LEAF_USER_ID) + '''\n''')
				openedFile.write('''startDatetime:''' + str(Globals.INFO_START_TIME) + '''\n''')
				openedFile.write('''finishDatetime:''' + str(Globals.INFO_FINISH_TIME) + '''\n''')
				openedFile.write('''stars:''' + str(Globals.INFO_STARS) + '''\n''')
				
			finally:
				# Se cierra el archivo, sin importar lo que haya pasado
				try:
					openedFile.close
				except:
					pass
			
			# Y se almaceno la informacion
			self.__dataProcessDefined = True
			
		elif self.__dataSentDefined == False:
			
			# Determinamos si hay un envio de batch en proceso
			if self.__sendBatchInProgress == False:
				
				# Armamos el JSON a enviar con los datos en batch
				fileLinesToProcess = None
				
				try:
					openedFile = None
					
					# Abrimos el archivo en modo lectura
					if olpcgames.ACTIVITY:  # Running as Activity
						name = os.getcwd() + '/UserInfo.txt'
						openedFile = open(name, 'r')
					else:
						openedFile = open('UserInfo.txt', 'r')
						
					# Escibimos el contenido apropiado
					fileLinesToProcess = openedFile.readlines()
					
				finally:
					# Se cierra el archivo, sin importar lo que haya pasado
					try:
						openedFile.close
					except:
						pass
					
				if (fileLinesToProcess == None) or (fileLinesToProcess == ""):
					
					# Falla en la creacion o envio del JSON
					self.__dataSentDefined = True
					return
				
				# Procesamos las lineas obtenidas:
				
				# Removemos los datos no relevantes en este momento: userId, username y password
				fileLinesToProcess = fileLinesToProcess[3:]
				
				# Variable para controlar la linea leida por bloque de informacion
				index = 0
				
				# Cadena con el batch de informacion a enviar
				batchDataToSend = ""
				
				for currentLine in fileLinesToProcess:
					
					if index == 0:  # Separador
						
						# La coma separadora solo se coloca despues de colocar el primer bloque
						if batchDataToSend != "":
							batchDataToSend = batchDataToSend + ''','''
						index = index + 1

					elif index == 1:  # Leaf User Id
						batchDataToSend = batchDataToSend + '''
							{ "leafUserId": "''' + currentLine[11:len(currentLine) - 1] + '''", '''
						index = index + 1

					elif index == 2:  # Start Datetime
						batchDataToSend = batchDataToSend + '''"startDatetime": "''' + currentLine[14:len(currentLine) - 1] + '''", '''
						index = index + 1
					
					elif index == 3:  # Finish Datetime
						batchDataToSend = batchDataToSend + '''"finishDatetime": "''' + currentLine[15:len(currentLine) - 1] + '''", '''
						index = index + 1

					elif index == 4:  # Stars
						batchDataToSend = batchDataToSend + '''"stars": "''' + currentLine[6:len(currentLine) - 1] + '''"}'''
						index = 0
					
				# Iniciamos el proceso de envio de los datos en batch
				try:
					# Parametros de conexion
					url = 'http://www.transformando.gov.co/api/public/index/batch'
					jsonParameters = '''
					{
						"gameId": "2",
						"rootUserId": "''' + str(Globals.INFO_ROOT_USER_ID) + '''",
						"data": [''' + batchDataToSend + '''
						]
					}'''
					parameters = urllib.urlencode({'data': jsonParameters})
					# Hacemos la solicitud por POST
					self.__sendBatchThread = ConnectionController(1, url, parameters)
					self.__sendBatchThread.start()
					
					# Levantamos la bandera correspondiente
					self.__sendBatchInProgress = True
					
				except:
					# Falla en la creacion o envio del JSON
					self.__dataSentDefined = True

			# Envio del batch en progreso            
			elif self.__sendBatchInProgress == True:
				
				# Si hay un hilo tratando de conectarse
				if self.__sendBatchThread != None:
					
					if self.__sendBatchThread.getState() == 1:
						# Esperamos hasta que se defina la situacion de la conexion
						pass
					
					elif self.__sendBatchThread.getState() == 2:
						
						# Datos en Batch enviados correctamente, ahora debemos eliminar del archivo el batch de datos enviados
						newFile = None
						
						# Creamos un archivo
						if olpcgames.ACTIVITY:  # Running as Activity
							name = os.getcwd() + '/UserInfo.txt'
							newFile = open(name, 'w+')
						else:
							newFile = open('UserInfo.txt', 'w+')
							
						# Escibimos el contenido apropiado
						newFile.write('''rootUserId:''' + str(Globals.INFO_ROOT_USER_ID) + '''\n''')
						newFile.write('''username:''' + str(Globals.INFO_USERNAME) + '''\n''')
						newFile.write('''password:''' + str(Globals.INFO_PASSWORD) + '''\n''')
						
						# Se cierra el archivo
						try:
							newFile.close
						except:
							pass
						
						# Levantamos la bandera para que comience el proceso de cerrado del juego                        
						self.__dataSentDefined = True 
						
					elif self.__sendBatchThread.getState() == 3:
						
						# Falla de la conexion
						self.__dataSentDefined = True

		# Ya se definio la situacion del batch de datos, ya puede comenzar el proceso de cerrado
		else:
			# Conteo para evitar Race Conditions y permitir el almacenamiento persistente
			# self.__count = self.__count + 1
				
			# if self.__count >= self.__endTime:
			Globals.thisGame.modeTimer = 150
	
	def checkIfIllustrated(self):
		q1 = Globals.thisLevel.qlist[Globals.questionId]
		if q1 == 2:
			return (1,182)
		elif q1 == 6:
			return (2,195)
		elif q1 == 10:
			return (3,244)
		elif q1 == 23:
			return (4,321)
		elif q1 == 16:
			return (5,195)
		elif q1 == 0:
			return (6,333)
		elif q1 == 3:
			return (7,295)
		elif q1 == 1:
			return (8,243)
		elif q1 == 33:
			return (9,402)
		elif q1 == 4:
			return (10,311)
		elif q1 == 7:
			return (11,326)
		else:
			return (0,0)

	def showDialog(self):
		if Globals.thisGame.modeTimer == 0:
			Globals.thisGame.modeTimer += 1
			self.quest = []
			self.ans1 = []
			self.ans2 = []
			self.ans3 = []
			self.quest = Globals.thisLevel.separateText(Globals.thisLevel.questions[Globals.questionId],57)
			self.ans1 = Globals.thisLevel.separateText(Globals.thisLevel.answers[Globals.questionId][0][0],50)
			self.ans2 = Globals.thisLevel.separateText(Globals.thisLevel.answers[Globals.questionId][1][0],50)
			self.ans3 = Globals.thisLevel.separateText(Globals.thisLevel.answers[Globals.questionId][2][0],50)
			#determinar si la pregunta esta ilustrada
			self.illustrated = self.checkIfIllustrated()
			if (self.illustrated[0] > 0):
				self.questionImg = pygame.image.load("res/sprite/p"+str(self.illustrated[0])+".png").convert_alpha()
			else:
				self.questionImg = pygame.image.load("res/sprite/pregunta.png").convert_alpha()
		#Muestra la interfaz de preguntas
		draw(self.backgroundQuestion,(0,0))
		if (self.illustrated[0] > 0):
			draw(self.questionImg,(self.illustrated[1],0))
		else:
			drawScaled(self.questionImg,(811,170),(195,131))
		paintMultiline(80,370,self.quest)
		draw(self.btn_a1,(90,500))
		draw(self.btn_b1,(90,580))
		draw(self.btn_c1,(90,660))
		paintMultiline(180,502,self.ans1)
		paintMultiline(180,582,self.ans2)
		paintMultiline(180,662,self.ans3)

	def checkDialogInput(self):
		if pygame.key.get_pressed()[ pygame.K_KP7 ] or pygame.key.get_pressed()[pygame.K_a]:
			self.checkAnswer(0)
		elif pygame.key.get_pressed()[ pygame.K_KP3 ] or pygame.key.get_pressed()[pygame.K_b]:
			self.checkAnswer(1)
		elif pygame.key.get_pressed()[ pygame.K_KP1 ] or pygame.key.get_pressed()[pygame.K_c]:
			self.checkAnswer(2)

	def checkAnswer(self,value):
		Globals.thisGame.modeTimer = 0
		self.questionImg = None
		if (Globals.thisLevel.answers[Globals.questionId][value][1] == 1):
			#respuesta correcta
			self.dyingPos = (Globals.ghosts[Globals.questionId].x+25,Globals.ghosts[Globals.questionId].y)
			del Globals.ghosts[Globals.questionId]
			self.dialog = 0
			Globals.thisGame.AddToScore(25)
			self.ghostDying = 1
			self.explosion.play()
			self.turnNormal()
			self.checkCompletion()
		else:
			#respuesta incorrecta
			self.dialog = 0
			self.tryAgain = 1
			self.restartPlayer()
		pygame.mixer.music.load(Globals.actualMusic)
		pygame.mixer.music.play(-1)

	def checkCompletion(self):
		#if len(Globals.thisLevel.items) < 1 and len(Globals.ghosts.items()) < 1:
		if len(Globals.thisLevel.items) < 1:
			Globals.ghosts = {}
			self.popup = pygame.image.load("res/backgrounds/fondo_caritas.png").convert_alpha()
			Globals.thisGame.SetMode(6)

			#modo rapido para pruebas
			#ranwin = random.randint(1,7)
			#self.winImg = pygame.image.load("res/sprite/congrats"+str(ranwin)+".png").convert_alpha()
			#Globals.thisGame.SetMode(7)

	def showEmotionTrivia(self):
		if Globals.thisGame.modeTimer == 0:
			Globals.thisGame.modeTimer += 1
			self.emotiontext = Globals.thisLevel.separateText(data.emotions[Globals.emotionnum][0],38)
		draw(self.popup,(13,30))
		draw(self.buttonstate,(530,535))
		self.instructions.doPaint()
		self.instructions1.doPaint()
		paintMultiline(105,240,self.emotiontext)
		thisface = pygame.image.load('res/sprite/'+Globals.selectedCharacter+'_em'+str(self.emotionSelected)+'.png')
		drawScaled(thisface,(240,351),(840,170))
		del thisface
		drawScaled(self.inst1,(268,80),(280,745))
		drawScaled(self.inst2,(268,80),(610,745))
		for event in pygame.event.get():
			if event.type == QUIT:
				Globals.thisGame.SetMode(10)
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_KP6 or event.key == pygame.K_RIGHT:
					self.emotionSelected += 1
					if self.emotionSelected == 19:
						self.emotionSelected = 1
				elif event.key == pygame.K_KP4 or event.key == pygame.K_LEFT:
					self.emotionSelected -= 1
					if self.emotionSelected == 0:
						self.emotionSelected = 18
				elif event.key == pygame.K_KP1 or event.key == pygame.K_RETURN:
					self.buttonstate = self.buttonDown
					if self.emotionSelected == data.emotions[Globals.emotionnum][1]:
						del self.popup
						Globals.thisGame.modeTimer = 0
						ranwin = random.randint(1,7)
						self.winImg = pygame.image.load("res/sprite/congrats"+str(ranwin)+".png").convert_alpha()
						Globals.thisGame.SetMode(7)
					else:
						self.errorSound.play()
		if pygame.key.get_pressed()[ pygame.K_ESCAPE ]:
			Globals.thisGame.SetMode(10)

	def CheckInputs(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				Globals.thisGame.SetMode(10)

		if Globals.thisGame.mode == 1 and self.dialog == 0:
			(xPos, yPos) = pygame.mouse.get_pos()
			if (xPos >= 1200 - 87) and (xPos <= 1200) and (yPos >= 0) and (yPos <= 0 + 74):
				Globals.thisGame.SetMode(10)
			if pygame.key.get_pressed()[pygame.K_KP6] or pygame.key.get_pressed()[pygame.K_RIGHT]:
				Globals.player.velX = Globals.player.speed
				Globals.player.velY = 0

			elif pygame.key.get_pressed()[ pygame.K_KP4 ] or pygame.key.get_pressed()[pygame.K_LEFT]:
				Globals.player.velX = -Globals.player.speed
				Globals.player.velY = 0

			elif pygame.key.get_pressed()[ pygame.K_KP2 ] or pygame.key.get_pressed()[pygame.K_DOWN]:
				Globals.player.velX = 0
				Globals.player.velY = Globals.player.speed

			elif pygame.key.get_pressed()[ pygame.K_KP8 ] or pygame.key.get_pressed()[pygame.K_UP]:
				Globals.player.velX = 0
				Globals.player.velY = -Globals.player.speed

			else:
				Globals.player.velX = 0
				Globals.player.velY = 0

		if pygame.key.get_pressed()[ pygame.K_ESCAPE ]:
			Globals.thisGame.SetMode(10)

	def restartPlayer(self):
		Globals.player.x = Globals.player.homeX
		Globals.player.y = Globals.player.homeY
		Globals.player.velX = 0
		Globals.player.velY = 0
		Globals.player.anim_pacmanCurrent = Globals.player.anim_pacmanS
		Globals.player.animFrame = 3
		self.turnNormal()

	def gameOver(self):
		print "gameover called"
		#self.timeOver = 1
		self.timeOverImg = pygame.image.load("res/sprite/timeOver.png").convert_alpha()
		Globals.thisGame.modeTimer = 0
		Globals.thisGame.SetMode(4)
				
	def turnNormal(self):
		Globals.player.state = 1
		Globals.player.speed = Globals.playerSpeed
		for k,item in Globals.ghosts.items():
			item.anim[2] = self.ghostNormalFrame

	def turnVulnerable(self):
		Globals.player.state = 2
		Globals.player.speed = Globals.playerSpeed + 3
		for k,item in Globals.ghosts.items():
			item.anim[2] = self.ghostVulnerableFrame

	def restorePowerups(self):
		for item in Globals.thisLevel.powerups:
			item[4] = 1

	def getRemainingTime(self):
		_tim = int(Globals.thisGame.timer / 30)
		_tim = 480 - _tim
		_mins = int(_tim/60)
		_secs = _tim % 60
		_strsecs = str(_secs)
		if _secs < 10:
			_strsecs = '0'+str(_secs)
		return str(_mins)+':'+_strsecs

	def drawPowerups(self):
		for item in Globals.thisLevel.powerups:
			if (item[4] == 1):
				draw(Globals.thisLevel.starIcon,(item[0]-Globals.thisGame.screenPixelPos[0], item[2]-Globals.thisGame.screenPixelPos[1]))
	#      _____________________________________________

	def showScreen(self,screenId):
		
		# Mostrar pantalla de registro o de login
		if screenId == 4:
			self.currentScreen = ScreenLogin()

		elif screenId == 5:
			self.currentScreen = ScreenRegistration()

		Globals.thisGame.SetMode(12)

	def goNextLevel(self):
		Globals.INFO_STARS += Globals.thisGame.score
		Globals.dificulty += 1
		Globals.emotionnum += 1
		if Globals.emotionnum > 9:
			Globals.emotionnum = 0
		if Globals.thisGame.levelNum == 1:
			Globals.thisGame.levelNum = random.randint(2,10)
		else:
			Globals.thisGame.levelNum = random.randint(1,10)
			#Globals.playerSpeed = 18
			#Globals.ghostSpeed = 18
			#Globals.player.speed = Globals.playerSpeed
		Globals.levelBoot = Globals.thisGame.levelNum
		Globals.thisLevel = Level()
		Globals.thisGame.StartNewGame(Globals.thisGame.levelNum)

	def run(self):
		Globals.player = Hero()
		Globals.thisGame = game()
		Globals.thisLevel = Level()
		#Empieza en el nivel 0 para que muestre los menus
		Globals.thisLevel.LoadLevel( Globals.thisGame.GetLevelNum() )
		#Globals.thisLevel.LoadLevel(Globals.levelBoot)
		pygame.mixer.music.set_volume(1)
		pygame.mixer.music.play(-1)

		self.ghostDieAnim = {}
		for i in range(1, 11, 1):
			self.ghostDieAnim[i] = pygame.image.load("res/sprite/exp"+str(i) + ".png").convert_alpha()

		# self.window = pygame.display.set_mode( Globals.thisGame.screenSize, SWSURFACE  )
		# self.window = pygame.display.set_mode( (1200,825), 0 ,0 )

		while True:

			#mode1: modo normal de juego
			if Globals.thisGame.mode == 1:
				#se mueve la imagen de fondo
				back_x = 0
				back_y = 0
				#if (Globals.thisLevel.levelSize - Globals.thisGame.screenPixelPos[0]) < Globals.thisLevel.levelOffset:
				#	back_x = -Globals.thisLevel.levelOffset
				#else:
				back_x = -Globals.thisGame.screenPixelPos[0]
				if (Globals.thisLevel.levelHeight - Globals.thisGame.screenPixelPos[1]) < Globals.thisLevel.heightOffset:
					back_y = -Globals.thisLevel.heightOffset
				else:
					back_y = -Globals.thisGame.screenPixelPos[1]
				draw(Globals.img_Background, (back_x, back_y),1)

				self.CheckInputs()
				if not self.dialog:
					Globals.player.Move()
					for item in Globals.thisLevel.items:
						if Globals.thisLevel.CheckIfHit((Globals.player.x,Globals.player.y),(item[0],item[2]),(25,21)):
							Globals.thisLevel.items.remove(item)
							Globals.thisGame.AddToScore(1)
							Globals.snd_item.play()
							self.checkCompletion()
							break
					
					for item in Globals.thisLevel.powerups:
						if Globals.thisLevel.CheckIfHit((Globals.player.x,Globals.player.y),(item[0],item[2]),(50,41)) and not item[4] == 0:
							item[4] = 0
							mytimer = Timer(10.0,self.turnNormal)
							mytimer.start()
							self.PUtimer = 1
							self.turnVulnerable()
							break
					
					for k,item in Globals.ghosts.items():
						if Globals.thisLevel.CheckIfHit( (Globals.player.x, Globals.player.y), (item.x, item.y), (50,90)):
							if Globals.player.state == 2:
								Globals.questionId = item.id
								self.dialog = 1
								Globals.player.state == 0
								pygame.mixer.music.load('res/sounds/Musica/preguntas.ogg')
								pygame.mixer.music.play(-1)
								Globals.player.velX = 0
								Globals.player.velY = 0
							elif Globals.player.state == 1:
								Globals.thisGame.AddToScore(-15)
								#if Globals.thisGame.score < 0:
								#	self.gameOver()
								#else:
								Globals.thisLevel.Restart()
								self.tryAgain = 1
					Globals.player.Draw()
					for k,item in Globals.ghosts.items():
						item.Move()
					if self.PUtimer > 0:
						self.PUtimer += 1
						if (self.PUtimer == 450):
							self.restorePowerups()

					#mostrar secuencia de explosion de fantasma
					if self.ghostDying:
						draw(self.ghostDieAnim[self.ghostDieFrame],(self.dyingPos[0] - Globals.thisGame.screenPixelPos[0],self.dyingPos[1] - Globals.thisGame.screenPixelPos[1]))
						self.ghostAnimTimer += 1
						if self.ghostAnimTimer == 4:
							self.ghostDieFrame += 1
							self.ghostAnimTimer = 1
						if self.ghostDieFrame == 11:
							self.ghostDieFrame = 1
							self.ghostDying = 0
					Globals.thisGame.SmartMoveScreen()
					Globals.thisLevel.drawItems()
					self.drawPowerups()
					for k,item in Globals.ghosts.items():
						item.Draw()
					if self.tryAgain:
						draw(self.tryAgainImg,(229,250))
						self.tryAgainTimer += 1
						if self.tryAgainTimer == 60:
							self.tryAgain = 0
							self.tryAgainTimer = 0

					#indicadores de items, siempre deben ir de ultimo
					draw(self.fondoItem,(0,0))
					draw(self.starIndicator,(5,10))
					self.__collectedItemsIndicator.setText('x '+str(Globals.thisGame.score))
					self.__collectedItemsIndicator.doPaint()
					draw(self.clockBack,(495,0))
					draw(self.clockImg,(500,3))
					self.__timeRemainingIndicator.setText(self.getRemainingTime())
					self.__timeRemainingIndicator.doPaint()
					
					Globals.thisGame.timer += 1
					if Globals.thisGame.timer == 17550:
						pygame.mixer.music.load("res/sounds/FX/reloj.ogg")
						pygame.mixer.music.play(-1)
					elif Globals.thisGame.timer == 18000:
						pygame.mixer.music.stop()
						self.timeOver = 1
						self.gameOver()
				else:
					self.showDialog()
					self.checkDialogInput()
						
			#mode3 : inicio del juego
			elif Globals.thisGame.mode == 3:
				self.CheckInputs()
				Globals.thisGame.modeTimer += 1
				#if Globals.thisGame.modeTimer == 1:
					#self.checkPersistence()
				if Globals.thisGame.modeTimer == 30:
					Globals.img_Background = pygame.image.load("res/backgrounds/Splash_2.png")
				elif Globals.thisGame.modeTimer == 60:
					Globals.img_Background = pygame.image.load("res/backgrounds/Splash_3.png")
				elif Globals.thisGame.modeTimer == 90:
					Globals.img_Background = pygame.image.load("res/backgrounds/Splash_4.png")
				elif Globals.thisGame.modeTimer == 120:
					Globals.img_Background = pygame.image.load("res/backgrounds/Splash_5.png")
				elif Globals.thisGame.modeTimer >= 150:
					#if self.persistenceChecked:
					#	self.showScreen(self.screenToGo)	
					Globals.thisGame.SetMode(9)
				draw(Globals.img_Background, (0, 0))
			
			#mode4 : tiempo terminado
			elif Globals.thisGame.mode == 4:
				if self.timeOver:
					#cargar imagen de timeover, verificar que cuando ya no se muestre, borrarla
					draw(self.timeOverImg,(229,264))
				Globals.thisGame.modeTimer += 1
				if Globals.thisGame.modeTimer == 150:
					#se reinicia el juego
					del self.timeOverImg
					Globals.thisGame.changeToLevel(1)

			#mode6 : pregunta emocional antes de terminar el nivel
			elif Globals.thisGame.mode == 6:
				# Globals.thisGame.SetMode(7)
				self.showEmotionTrivia()

			#mode7 : pausa entre niveles, muestra el aviso de felicitaciones
			elif Globals.thisGame.mode == 7:
				Globals.thisGame.modeTimer += 1
				draw(self.winImg,(111, 25))
				if Globals.thisGame.modeTimer == 200:
					self.goNextLevel()

			#mode9 : pantalla de tutorial antes de iniciar el primer nivel
			elif Globals.thisGame.mode == 9:
				if Globals.thisGame.modeTimer == 0:
					self.currentScreen = None
					back = pygame.image.load("res/backgrounds/tutorial.png").convert()
					Globals.thisGame.modeTimer += 1
				draw(back,(0,0))
				for event in pygame.event.get():
					if event.type == QUIT:
						Globals.thisGame.SetMode ( 10 )
					elif event.type == pygame.KEYDOWN:
						if event.key == pygame.K_KP1 or event.key == pygame.K_RETURN:
							Globals.thisGame.SetMode(2)

			#mode2 : pantalla de seleccion de personaje
			elif Globals.thisGame.mode == 2:
				if Globals.thisGame.modeTimer == 0:
					back = pygame.image.load("res/backgrounds/select_gender.png").convert()
					gm1 = pygame.image.load("res/sprite/select_gender_m1.png").convert_alpha()
					gm2 = pygame.image.load("res/sprite/select_gender_m2.png").convert_alpha()
					gw1 = pygame.image.load("res/sprite/select_gender_w1.png").convert_alpha()
					gw2 = pygame.image.load("res/sprite/select_gender_w2.png").convert_alpha()
					Globals.thisGame.modeTimer += 1
				draw(back,(0,0))
				if Globals.selectedCharacter == 'm':
					draw(gm1,(204,88))
					draw(gw2,(561,88))
				else:
					draw(gm2,(204,88))
					draw(gw1,(561,88))
				drawScaled(self.inst1,(268,80),(280,745))
				drawScaled(self.inst2,(268,80),(610,745))


				for event in pygame.event.get():
					if event.type == QUIT:
						Globals.thisGame.SetMode ( 10 )
					elif event.type == pygame.KEYDOWN:
						if event.key == pygame.K_KP6 or event.key == pygame.K_RIGHT:
							Globals.selectedCharacter = 'w'
						elif event.key == pygame.K_KP4 or event.key == pygame.K_LEFT:
							Globals.selectedCharacter = 'm'
						elif event.key == pygame.K_KP1 or event.key == pygame.K_RETURN:
							del gm1
							del gm2
							del gw1
							del gw2
							Globals.player = Hero()
							Globals.thisGame.modeTimer = 0
							Globals.thisGame.StartNewGame(1)

			#mode10 : secuencia de salida del juego
			elif Globals.thisGame.mode == 10:
				for event in pygame.event.get():
					if event.type == QUIT:
						pass
				if Globals.thisGame.modeTimer == 0:
					Globals.img_Background = pygame.image.load("res/backgrounds/Splash_final.png")
					draw(Globals.img_Background,(0,0))
					self.savePersistence()
				elif Globals.thisGame.modeTimer == 150:
					sys.exit(0)

			#mode12 : modo de pantalla de login o registro
			elif Globals.thisGame.mode == 12:
				self.currentScreen.doTask()
				self.currentScreen.doPaint()
				# self.CheckInputs()
			pygame.display.update()
			self.clock.tick (30)

class Text:
	def __init__(self, fontName, size, text, color, lx,ly):
		self.__font = pygame.font.Font('res/BorisBlackBloxx.ttf',35)
		self.__text = text
		self.__color = color
		self.__positionX = lx
		self.__positionY = ly

	def doPaint(self):
		text = unicode(self.__text, "UTF-8")
		draw(self.__font.render(text, 1, self.__color), (self.__positionX, self.__positionY))

	def setText(self, newText):
		self.__text = newText

class ghost():
	def __init__ (self, ghostID):
		self.x = 0
		self.y = 0
		self.velX = 0
		self.velY = 0
		self.speed = Globals.ghostSpeed
		self.nearestRow = 0
		self.nearestCol = 0
		self.id = ghostID
		self.timer = 0
		self.homeX = 0
		self.homeY = 0
		self.currentPath = "L"
		self.anim = {}
		for i in range(1, 5, 1):
			self.anim[i] = pygame.image.load("res/sprite/ghost" + str(i) + ".png")
		self.animFrame = 1
		self.animDelay = 0

	def Draw (self):
		if not Globals.thisGame.mode == 1:
			return False

		draw(self.anim[ self.animFrame ], (self.x - Globals.thisGame.screenPixelPos[0], self.y - Globals.thisGame.screenPixelPos[1]))

		#if Globals.thisGame.mode == 6 or Globals.thisGame.mode == 7:
			# don't animate ghost if the level is complete
			#return False

		self.animDelay += 1

		if self.animDelay == 2:
			self.animFrame += 1

			if self.animFrame == 5:
				self.animFrame = 1
				
			self.animDelay = 0

	def Move (self):
		self.nearestRow = int(((self.y + 50) / 25))
		self.nearestCol = int(((self.x + 25) / 25))
		if not Globals.thisLevel.CheckIfHitWall((self.x+self.velX,self.y+self.velY), (50,100)):
			self.x += self.velX
			self.y += self.velY
			self.timer += 1
			if (self.timer >= 60):
				self.getRandomWay()
				self.timer = 0
		else:
			self.getRandomWay()

	def getRandomWay(self):
		ran = random.randint(0,4)
		if ran == 0:
			self.currentPath = 'L'
			(self.velX, self.velY) = (-self.speed, 0)
		elif ran == 1:
			self.currentPath = 'U'
			(self.velX, self.velY) = (0,-self.speed)
		elif ran == 2:
			self.currentPath = 'R'
			(self.velX, self.velY) = (self.speed, 0)
		elif ran == 3:
			self.currentPath = 'D'
			(self.velX, self.velY) = (0, self.speed)

def draw(target,(x,y),override=0):
	if override == 1:
		Globals.screen.blit(target,(x,y))
	elif x >= 0 and x < 1200 and y >= 0 and y < 825:
		Globals.screen.blit(target,(x,y))

def drawScaled(target,(w,h),(x,y)):
	item = pygame.transform.scale(target,(w,h))
	Globals.screen.blit(item,(x,y))

def paintMultiline(left,top,texts):
	for et in texts:
		line = Text(None, 40, et, (255, 255, 255), left, top)
		line.doPaint()
		top += 33

class Label:
 
	def __init__(self, text, size, color, positionXY):
		self.text = text
		self.__font = pygame.font.Font('res/BorisBlackBloxx.ttf',size)
		self.__color = color
		self.__positionXY = positionXY
 
	def doPaint(self):
		if self.text != "":
			text = unicode(self.text, "UTF-8")
			renderedText = self.__font.render(text, 1, self.__color)
			draw(renderedText, (self.__positionXY[0], self.__positionXY[1]))

	def setText(self, newText):
		self.text = newText
		
	def setColor(self, newColor):
		self.__color = newColor
		
	def setPosition(self, positionXY):
		self.__positionXY = positionXY
		
	def getPosition(self):
		return self.__positionXY
		
	def addChar(self, charToAdd):
		self.text = self.text + charToAdd
		
	def delLastChar(self):
		if len(self.text) > 0:
			self.text = self.text[:len(self.text) - 1]        
		
	def getTextLen(self):
		return len(self.text)
	
	def getTextRenderLen(self):
		return self.__font.size(self.text)[0]

class TextBox:

	def __init__(self, posX, posY, width, maxChars, font, isPassword, displaySurface):
		self.displaySurface = displaySurface
		self.__posX = posX
		self.__posY = posY
		
		self.__focusBorderColor = (255, 255, 0)
		self.__normalBorderColor = (48, 116, 135)
		self.__contentColor = (147, 212, 192)
		self.__textColor = (38, 95, 110)
		
		self.__textReal = Label("", font, self.__textColor, (posX, posY))
		self.__textPassword = Label("", font, self.__textColor, (posX, posY))
		
		self.__maxChars = maxChars
		self.__focus = False
		self.__uppercase = False
		self.__isPassword = isPassword
		
		fontValue = font
			
		self.__height = fontValue * 1.5
		self.__width = width
		
		self.__normalBorderWidth = 4
		self.__focusBorderWidth = self.__normalBorderWidth * 2
		
	def getText(self):
		return self.__textReal.text
		
	def doTask(self):
		pass
	
	def doPaint(self):
		
		# Borde de Foco
		if self.__focus == True:
			pygame.draw.rect(self.displaySurface, self.__focusBorderColor, pygame.Rect(self.__posX - self.__focusBorderWidth, self.__posY - self.__focusBorderWidth, self.__width + (self.__focusBorderWidth * 2), self.__height + (self.__focusBorderWidth * 2)))
		
		# Borde
		pygame.draw.rect(self.displaySurface, self.__normalBorderColor, pygame.Rect(self.__posX - self.__normalBorderWidth, self.__posY - self.__normalBorderWidth, self.__width + (self.__normalBorderWidth * 2), self.__height + (self.__normalBorderWidth * 2)))
		
		# Contenido
		pygame.draw.rect(self.displaySurface, self.__contentColor, pygame.Rect(self.__posX, self.__posY, self.__width, self.__height))
		
		# Texto ingresado
		if self.__isPassword == False:
			self.__textReal.doPaint()
		else:
			self.__textPassword.doPaint()
			
	def takeFocus(self):
		self.__focus = True
	
	def quitFocus(self):
		self.__focus = False

	def doMouseAction(self, event):
		
		# Detectamos la posicion en X y Y del click
		xPos, yPos = event.pos
		
		if (xPos >= self.__posX) and (xPos <= self.__posX + self.__width) and (yPos >= self.__posY) and (yPos <= self.__posY + self.__height):
			self.__focus = True
		else:
			self.__focus = False

	def doKeyAction(self, event):
		if self.__focus == True:

			# Teclas no permitidas                
			if event.key == pygame.K_TAB:
				pass
			elif event.key == pygame.K_CAPSLOCK:
				pass
			elif event.key == pygame.K_RETURN:
				pass
			
			# Eliminacion de un caracter
			elif event.key == pygame.K_BACKSPACE:
				self.__textReal.delLastChar()
				self.__textPassword.delLastChar()
				
			# Letra valida presionada
			elif event.key <= 255 and (self.__textReal.getTextLen() < self.__maxChars):
				
				# Obtenemos la letra
				charToAdd = chr(event.key)
				
				# Mayusculas
				if self.__uppercase == True:
					charToAdd = charToAdd.upper()
					# self.__uppercase = False
				
				# Añadimos la letra a la cadena
				self.__textReal.addChar(charToAdd)
				self.__textPassword.addChar("*")
				
	def switchCase(self):
		if self.__uppercase == True:
			self.__uppercase = False
		else:
			self.__uppercase = True

class Level:
	def __init__(self):
		self.lvlWidth = 0
		self.lvlHeight = 0
		self.map = {}
		self.fruitType = 0
		self.items = []
		self.powerups = []
		self.thisFruit = pygame.image.load("res/sprite/star.png")
		self.pellets = 0
		self.levelNum = 0
		self.qlist = []
		self.hittimer = 0
		self.walltimer = 0

	def SetMapTile (self, (row, col), newValue):
		self.map[ (row * self.lvlWidth) + col ] = newValue

	def GetMapTile (self, (row, col)):
		if row >= 0 and row < self.lvlHeight and col >= 0 and col < self.lvlWidth:
			return self.map[ (row * self.lvlWidth) + col ]
		else:
			return 0

	def getItem(self,row,col):
		for item in range(0,len(self.items),1):
			if (self.items[item][0] == col and self.items[item][1] == row):
				return item

	def IsWall (self, (row, col)):
		if row > self.lvlHeight - 1 or row < 0:
			return True
		if col > self.lvlWidth - 1 or col < 0:
			return True
		result = self.GetMapTile((row, col))
		if result == 1:
			return True
		else:
			return False

	#TODO: esta funcion debe ser lo mas optima posible, es llamada mucho
	def CheckIfHitWall (self, (possibleX, possibleY), (width, height)):
		numCollisions = 0
		ppr = possibleX+width
		ppb = possibleY+height
		leftCol = int(possibleX/25)
		rightCol = int(ppr/25)+1
		topRow = int(possibleY/25)
		bottomRow = int(ppb/25)+1
		for iRow in range(topRow, bottomRow, 1):
			for iCol in range(leftCol, rightCol, 1):
				if  (possibleX - (iCol * 25) < 25) and (ppr - (iCol * 25) > -25) and (possibleY - (iRow * 25) < 25) and (ppb - (iRow * 25) > -25):
					if self.IsWall((iRow, iCol)):
						numCollisions += 1
		if numCollisions > 0:
			return True
		else:
			return False
	
	#TODO: esta funcion debe ser lo mas optima posible, es llamada mucho
	def CheckIfHit (self, (playerX, playerY), (x, y), (w,h)):
		ppr = playerX+56
		ppb = playerY+99
		rl = x + w
		dl = y + h
		if (((playerX <= x and ppr > x) or (ppr >= rl and playerX < rl) or (playerX <= x and ppr > rl)) and ((playerY <= y and ppb > dl) or (playerY >= y and playerY < dl) or (playerY <= y and ppb > y))):
			return True
		else:
			return False

	def DrawMap (self):
		for row in range(-1, Globals.thisGame.tilesY +1, 1):
			outputLine = ""
			for col in range(-1, Globals.thisGame.tilesX +1, 1):
				actualRow = Globals.thisGame.screenNearestTilePos[0] + row
				actualCol = Globals.thisGame.screenNearestTilePos[1] + col
				useTile = self.GetMapTile((actualRow, actualCol))
				if useTile == 2:
					Globals.screen.blit (Globals.tileIDImage[ useTile ], (col * 25 - Globals.thisGame.screenPixelOffset[0], row * 25 - Globals.thisGame.screenPixelOffset[1]) )
	
	def drawItems(self):
		for i in range(0,len(self.items),1):
			_x = self.items[i][0]-Globals.thisGame.screenPixelPos[0]
			_y = self.items[i][2]-Globals.thisGame.screenPixelPos[1]
			draw(self.thisFruit,(_x, _y))

	def separateText(self,text,max_len):
		#dividir el texto por espacios
		lines = []
		entire_text = text.split(' ')
		liner = ''
		for each_line in entire_text:
			if len(liner) < max_len and (len(liner) + len(each_line) + 1) < max_len:
				liner += ' ' + each_line
			else:
				lines.append(str(liner))
				liner = each_line
		lines.append(liner)
		return lines

	def LoadLevel (self, levelNum):
		self.map = {}
		self.actions = []
		self.items = []
		self.questions = []
		self.answers = []
		Globals.thisGame.timer = 0
		f = open("res/levels/" + str(levelNum) + ".csv", 'r')
		#TODO: Fix everything here
		if (levelNum > 0):
			for qi in range(0, Globals.dificulty, 1):
				ql = Globals.questionnum + qi
				self.qlist.append(ql)
				self.questions.append(data.questions[ql])
				self.answers.append(data.answers[ql])
			Globals.questionnum += Globals.dificulty
		pygame.mixer.music.stop()
		pupImg = random.randint(1,7)
		self.starIcon = pygame.image.load("res/tiles/"+Globals.itemTypes[pupImg]+".png").convert_alpha()
		if levelNum > 0:
			Globals.img_Background = pygame.image.load("res/backgrounds/"+ str(levelNum) +".png")
			Globals.actualMusic = 'res/sounds/Musica/music'+str(random.randint(1,3))+'.ogg'
			pygame.mixer.music.load(Globals.actualMusic)
			pygame.mixer.music.set_volume(1)
			pygame.mixer.music.play(-1)
		self.powerups = []
		self.ghostsPositions = []
		#se crean los fantasmas y se les asigna un ID
		for i in range(0, Globals.dificulty, 1):
			Globals.ghosts[i] = ghost(i)
		ghostsIds = Globals.dificulty-1
		lineNum=-1
		rowNum = 0
		useLine = False
		isReadingLevelData = False
		for line in f:
			lineNum += 1
			while len(line)>0 and (line[-1]=="\n" or line[-1]=="\r"): line=line[:-1]
			while len(line)>0 and (line[0]=="\n" or line[0]=="\r"): line=line[1:]
			str_splitBySpace = line.split(' ')
			j = str_splitBySpace[0]
			if (j == "'" or j == ""):
				useLine = False
			elif j == "#":
				useLine = False
				firstWord = str_splitBySpace[1]
				if firstWord == "lvlwidth":
					self.lvlWidth = int( str_splitBySpace[2] )
					self.levelSize = self.lvlWidth * 25
					self.levelOffset = self.levelSize - Globals.thisGame.screenSize[0]
				elif firstWord == "lvlheight":
					self.lvlHeight = int( str_splitBySpace[2] )
					self.levelHeight = self.lvlHeight * 25
					self.heightOffset = self.levelHeight - Globals.thisGame.screenSize[1]
				elif firstWord == "startleveldata":
					isReadingLevelData = True
					rowNum = 0
				elif firstWord == "endleveldata":
					isReadingLevelData = False
			else:
				useLine = True
			if useLine == True:
				if isReadingLevelData == True:
					for k in range(0, self.lvlWidth, 1):
						self.SetMapTile((rowNum, k), int(str_splitBySpace[k]) )
						thisID = int(str_splitBySpace[k])
						_x = k *25
						_y = rowNum * 25

						#posicion incial del jugador
						if thisID == 4:
							Globals.player.homeX = _x
							Globals.player.homeY = _y
							self.SetMapTile((rowNum, k), 0 )

						elif thisID == 5:
							self.ghostsPositions.append([_x,_y])
							self.SetMapTile((rowNum, k), 0 )

						#colocar una estrella pequeña
						elif thisID == 2:
							temp1 = _x + 25
							temp2 = _y + 21
							self.items.append([_x,temp1,_y,temp2])
							self.pellets += 1

						elif thisID == 3:
							temp1 = _x + 50
							temp2 = _y + 50
							self.powerups.append([_x,temp1,_y,temp2,1])
					rowNum += 1
		#poner los fantasmas en las posiciones posibles
		pos = len(self.ghostsPositions)

		for g,item in Globals.ghosts.items():
			pos -= 1
			if pos < 0:
				pos = len(self.ghostsPositions)-1
			if pos >= 0:
				item.homeX = self.ghostsPositions[pos][0]
				item.homeY = self.ghostsPositions[pos][1]
		Globals.GetCrossRef()
		self.Restart()
		
	def Restart (self):
		for k,item in Globals.ghosts.items():
			item.x = item.homeX
			item.y = item.homeY
			item.velX = 0
			item.velY = 0
			item.state = 1
			item.speed = Globals.ghostSpeed
			item.Move()
			item.getRandomWay()
			
		Globals.player.x = Globals.player.homeX
		Globals.player.y = Globals.player.homeY
		Globals.player.velX = 0
		Globals.player.velY = 0
		Globals.player.anim_pacmanCurrent = Globals.player.anim_pacmanS
		Globals.player.animFrame = 3

class ScreenLogin:

	def __init__(self):
		
		# Input
		self.__loginInProgress = False
		self.__textboxUser = TextBox(385, 525, 440, 20, 30, False,Juego().window)
		self.__textboxPass = TextBox(385, 646, 440, 20, 30, True,Juego().window)
		
		# Login Control
		self.__loginStatus = Label("", 18, (255, 200, 200), (0, 796))
		self.__showLoginControls = False
		
		# User Checked
		self.__userCheck = False
		self.__userCheckTotalTime = 20
		self.__userCheckCurrentTime = 1
		
		# Hover
		self.__hoverCloseGame = False
		self.__hoverLoginButton = False
		self.__hoverLoginMainUser = False
		self.__hoverLoginParent = False
		self.__hoverLoginUncle = False
		self.__hoverLoginBrother = False
		self.__hoverLoginCousin = False
		self.__hoverLoginFriend = False

		self.background_Login = pygame.image.load("res/screens/Login.png").convert()
		self.input_LoginInput = pygame.image.load("res/screens/LoginInput.png").convert_alpha()
		self.input_Login_On = pygame.image.load("res/screens/Login_On.png").convert_alpha()
		self.input_Login_Off = pygame.image.load("res/screens/Login_Off.png").convert_alpha()
		self.input_Connecting = pygame.image.load("res/screens/Connecting.png").convert_alpha()
		self.input_LoginMainUser = pygame.image.load("res/screens/LoginMainUser.png").convert_alpha()
		self.input_LoginParent = pygame.image.load("res/screens/LoginParent.png").convert_alpha()
		self.input_LoginUncle = pygame.image.load("res/screens/LoginUncle.png").convert_alpha()
		self.input_LoginBrother = pygame.image.load("res/screens/LoginBrother.png").convert_alpha()
		self.input_LoginCousin = pygame.image.load("res/screens/LoginCousin.png").convert_alpha()
		self.input_LoginFriend = pygame.image.load("res/screens/LoginFriend.png").convert_alpha()
		self.input_CloseGame_On = pygame.image.load("res/screens/CloseGame_On.png").convert_alpha()
		self.input_CloseGame_Off = pygame.image.load("res/screens/CloseGame_Off.png").convert_alpha()

		pygame.mouse.set_visible(True)

	def doTask(self):
		
		# Mouse Hover Detection
		(xPos, yPos) = pygame.mouse.get_pos()
		
		# Outside
		self.__hoverCloseGame = False
		self.__hoverLoginButton = False
		self.__hoverLoginMainUser = False
		self.__hoverLoginParent = False
		self.__hoverLoginUncle = False
		self.__hoverLoginBrother = False
		self.__hoverLoginCousin = False
		self.__hoverLoginFriend = False
		
		# Close Game
		if (xPos >= 1200 - 87) and (xPos <= 1200) and (yPos >= 0) and (yPos <= 0 + 74): 
			self.__hoverCloseGame = True
		# Login Button
		elif (xPos >= 420) and (xPos <= 420 + 330) and (yPos >= 730) and (yPos <= 730 + 65) and (self.__showLoginControls == True):
			self.__hoverLoginButton = True
		# Main User
		elif (xPos >= 325) and (xPos <= 325 + 540) and (yPos >= 450) and (yPos <= 450 + 350) and (self.__showLoginControls == False):
			self.__hoverLoginMainUser = True
		# Parents
		elif (xPos >= 495) and (xPos <= 495 + 248) and (yPos >= 110) and (yPos <= 110 + 158):
			self.__hoverLoginParent = True
		# Uncle
		elif (xPos >= 750) and (xPos <= 750 + 246) and (yPos >= 190) and (yPos <= 190 + 156):
			self.__hoverLoginUncle = True
		# Brother
		elif (xPos >= 245) and (xPos <= 245 + 246) and (yPos >= 190) and (yPos <= 190 + 156):
			self.__hoverLoginBrother = True
		# Cousin
		elif (xPos >= 58) and (xPos <= 58 + 246) and (yPos >= 344) and (yPos <= 344 + 156):
			self.__hoverLoginCousin = True
		# Friend
		elif (xPos >= 922) and (xPos <= 922 + 246) and (yPos >= 345) and (yPos <= 345 + 156):
			self.__hoverLoginFriend = True
			
		# Si el usuario ya ha sido verificado
		if self.__userCheck == True:
			if self.__userCheckCurrentTime < self.__userCheckTotalTime:
				self.__userCheckCurrentTime = self.__userCheckCurrentTime + 1
			else:
				Globals.thisGame.SetMode(9)
		
		# Detectamos todos los eventos y ejecutamos las acciones correspondientes
		if pygame.event:
			for event in pygame.event.get():
				 
				# Evento cerrar el juego
				if event.type == pygame.QUIT:
					Globals.thisGame.SetMode(10)
					
				# Deteccion de click de mouse
				elif event.type == pygame.MOUSEBUTTONDOWN:
					self.__doMouseAction(event)
					
				# Deteccion de teclas presionadas
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						Globals.thisGame.SetMode(10)
					elif event.key == pygame.K_RSHIFT:
						self.__switchCase()
					elif event.key == pygame.K_LSHIFT:
						self.__switchCase()
					else:
						self.__doKeyAction(event)
						
	def doPaint(self):
		
		# Background
		draw(self.background_Login, (0, 0))

		if self.__showLoginControls == True:
			
			# Background
			draw(self.input_LoginInput, (163, 320))
			
			# TextBox
			self.__textboxUser.doPaint()
			self.__textboxPass.doPaint()
		
			# Buttons with Hover
			if self.__loginInProgress == False:
				if self.__hoverLoginButton == True:
					draw(self.input_Login_On, (420, 730))
				else:
					draw(self.input_Login_Off, (420, 730))
			else:
				draw(self.input_Connecting, (420, 730))
		else:
			if self.__hoverLoginMainUser == True:
				draw(self.input_LoginMainUser, (310, 345))
			
		if self.__hoverLoginParent == True:
			draw(self.input_LoginParent, (485, 74))
			
		if self.__hoverLoginUncle == True:
			draw(self.input_LoginUncle, (740, 150))
			
		if self.__hoverLoginBrother == True:
			draw(self.input_LoginBrother, (230, 150))
			
		if self.__hoverLoginCousin == True:
			draw(self.input_LoginCousin, (45, 305))
			
		if self.__hoverLoginFriend == True:
			draw(self.input_LoginFriend, (910, 305))
			
		# Login Status
		self.__loginStatus.doPaint()
		
		if self.__hoverCloseGame == True:
			draw(self.input_CloseGame_On, (1200 - 87, 0))
		else:
			draw(self.input_CloseGame_Off, (1200 - 87, 0))
				
	def __doKeyAction(self, event):
		
		# Si no hay algun evento en progreso...
		if self.__userCheck == False:
			
			self.__textboxUser.doKeyAction(event)
			self.__textboxPass.doKeyAction(event)
		
	def __doMouseAction(self, event):
		
		if self.__userCheck == False:
		
			# Removemos el foco de todas la cajas de texto
			self.__textboxUser.quitFocus()
			self.__textboxPass.quitFocus()
			
			# Detectamos la posicion en X y Y del click
			xPos, yPos = event.pos
	
			# Close Game
			if (xPos >= 1200 - 87) and (xPos <= 1200) and (yPos >= 0) and (yPos <= 0 + 74):
				
				Globals.thisGame.SetMode(10)
			
			# Login Button
			elif (xPos >= 420) and (xPos <= 420 + 330) and (yPos >= 730) and (yPos <= 730 + 65) and (self.__showLoginControls == True):
				
				# Reiniciamos esta bandera dado que un nuevo proceso de verificacion de usuario va a comenzar
				self.__userCheck = False
		
				# Reiniciamos los mensajes de estado
				self.__loginStatus.setText("")
				
				# Obtenemos los datos ingresados
				username = self.__textboxUser.getText()
				password = self.__textboxPass.getText()
				
				# Verificamos si todos los datos fueron ingresados
				if (username == "") or (password == ""):
					self.__loginStatus.setText("Se deben llenar todos los campos.")
					self.__loginStatus.setPosition((585 - (self.__loginStatus.getTextRenderLen() / 2), self.__loginStatus.getPosition()[1]))
					return
				
				# Verificamos que los datos ingresados correspondan con los persistidos
				if (Globals.INFO_USERNAME == username) and (Globals.INFO_PASSWORD == password):
					self.__loginStatus.setText("Login exitoso. Ingresando al juego...")
					self.__loginStatus.setPosition((585 - (self.__loginStatus.getTextRenderLen() / 2), self.__loginStatus.getPosition()[1]))
					
					# Indicamos el usuario que va a jugar
					Globals.INFO_LEAF_USER_ID = 0
					Globals.INFO_START_TIME = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")  
					
					# Levantamos la bandera correspondiente
					self.__userCheck = True
					
				else:
					self.__loginStatus.setText("Datos incorrectos.")
					self.__loginStatus.setPosition((585 - (self.__loginStatus.getTextRenderLen() / 2), self.__loginStatus.getPosition()[1]))
			
			# Main User
			elif (xPos >= 325) and (xPos <= 325 + 540) and (yPos >= 450) and (yPos <= 450 + 350) and (self.__showLoginControls == False):
				self.__showLoginControls = True
				self.__textboxUser.takeFocus()
				
			# Parents
			elif (xPos >= 495) and (xPos <= 495 + 248) and (yPos >= 110) and (yPos <= 110 + 158):
				# Indicamos el usuario que va a jugar
				Globals.INFO_LEAF_USER_ID = 1
				Globals.INFO_START_TIME = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
				
				# Cambiamos a la pantalla correspondiente
				Globals.thisGame.SetMode(9)
				
			# Uncle
			elif (xPos >= 750) and (xPos <= 750 + 246) and (yPos >= 190) and (yPos <= 190 + 156):
				# Indicamos el usuario que va a jugar
				Globals.INFO_LEAF_USER_ID = 2
				Globals.INFO_START_TIME = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
								
				# Cambiamos a la pantalla correspondiente
				Globals.thisGame.SetMode(9)
				
			# Brother
			elif (xPos >= 245) and (xPos <= 245 + 246) and (yPos >= 190) and (yPos <= 190 + 156):
				# Indicamos el usuario que va a jugar
				Globals.INFO_LEAF_USER_ID = 3
				Globals.INFO_START_TIME = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
				
				# Cambiamos a la pantalla correspondiente
				Globals.thisGame.SetMode(9)
				
			# Cousin
			elif (xPos >= 58) and (xPos <= 58 + 246) and (yPos >= 344) and (yPos <= 344 + 156):
				# Indicamos el usuario que va a jugar
				Globals.INFO_LEAF_USER_ID = 4
				Globals.INFO_START_TIME = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
				
				# Cambiamos a la pantalla correspondiente
				Globals.thisGame.SetMode(9)
				
			# Friend
			elif (xPos >= 922) and (xPos <= 922 + 246) and (yPos >= 345) and (yPos <= 345 + 156):
				# Indicamos el usuario que va a jugar
				Globals.INFO_LEAF_USER_ID = 5
				Globals.INFO_START_TIME = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
				
				# Cambiamos a la pantalla correspondiente
				Globals.thisGame.SetMode(9)
					
			# Textbox
			else:
				self.__textboxUser.doMouseAction(event)
				self.__textboxPass.doMouseAction(event)
		
	def __switchCase(self):
		if self.__userCheck == False:
			self.__textboxUser.switchCase()
			self.__textboxPass.switchCase()

class ScreenRegistration:

	def __init__(self):
		
		# Registration Input
		self.__textboxNames = TextBox(110, 148+20, 440, 20, 30, False,Juego().window)
		self.__textboxAge = TextBox(110, 263+20, 150, 2, 30, False,Juego().window)
		self.__textboxSchool = TextBox(110, 375+20, 440, 20, 30, False,Juego().window)
		self.__textboxGrade = TextBox(110, 487+20, 440, 20, 30, False,Juego().window)
		
		self.__textboxUsername = TextBox(620, 148+20, 440, 20, 30, False,Juego().window)
		self.__textboxPassword1 = TextBox(620, 263+20, 440, 20, 30, True,Juego().window)
		self.__textboxPassword2 = TextBox(620, 375+20, 440, 20, 30, True,Juego().window)
		self.__textboxNames.takeFocus()
		
		# Registration Control
		self.__registrationThread = None
		self.__registrationInProgress = False
		self.__registrationStatus = Label("", 18, (255, 200, 200), (0, 445))
		
		# Login Input
		self.__textboxLoginUsername = TextBox(110, 682+50, 340, 20, 30, False,Juego().window)
		self.__textboxLoginPassword = TextBox(750, 682+50, 350, 20, 30, True,Juego().window)
		
		# Login Control
		self.__loginThread = None
		self.__loginInProgress = False
		self.__loginStatus = Label("", 18, (255, 200, 200), (770, 770))
		
		# User Checked
		self.__userCheck = False
		self.__userCheckTotalTime = 20
		self.__userCheckCurrentTime = 1
		
		# Hover
		self.__hoverCloseGame = False
		self.__hoverRegistration = False
		self.__hoverLoginButton = False

		self.background_Registration = pygame.image.load("res/screens/Registration.png").convert()
		self.input_Registration_On = pygame.image.load("res/screens/Registration_On.png").convert_alpha()
		self.input_Registration_Off = pygame.image.load("res/screens/Registration_Off.png").convert_alpha()
		self.input_Connecting = pygame.image.load("res/screens/Connecting.png").convert_alpha()
		self.input_Login_On = pygame.image.load("res/screens/Login_On.png").convert_alpha()
		self.input_Login_Off = pygame.image.load("res/screens/Login_Off.png").convert_alpha()
		self.input_CloseGame_On = pygame.image.load("res/screens/CloseGame_On.png").convert_alpha()
		self.input_CloseGame_Off = pygame.image.load("res/screens/CloseGame_Off.png").convert_alpha()

		pygame.mouse.set_visible(True)
		
	def doTask(self):
		
		# Mouse Hover Detection
		(xPos, yPos) = pygame.mouse.get_pos()
		
		# Outside
		self.__hoverCloseGame = False
		self.__hoverRegistration = False
		self.__hoverLoginButton = False
		
		# Close Game
		if (xPos >= 1200 - 87) and (xPos <= 1200) and (yPos >= 0) and (yPos <= 0 + 74): 
			self.__hoverCloseGame = True
		# Registration Button
		elif (xPos >= 670) and (xPos <= 670 + 330) and (yPos >= 475) and (yPos <= 475 + 65):
			self.__hoverRegistration = True
		# Login Button
		elif (xPos >= 435) and (xPos <= 435 + 330) and (yPos >= 750) and (yPos <= 750 + 65):
			self.__hoverLoginButton = True

		# Si el usuario ya ha sido verificado
		if self.__userCheck == True:
			if self.__userCheckCurrentTime < self.__userCheckTotalTime:
				self.__userCheckCurrentTime = self.__userCheckCurrentTime + 1
			else:
				Globals.thisGame.SetMode(9)

		# Determinamos si hay un registro en proceso
		elif self.__registrationInProgress == True:
			
			# Si hay un hilo tratando de conectarse
			if self.__registrationThread != None:
				
				if self.__registrationThread.getState() == 1:
					
					if self.__registrationStatus.text == "Conectando":
						self.__registrationStatus.setText("Conectando.")
					elif self.__registrationStatus.text == "Conectando.":
						self.__registrationStatus.setText("Conectando..")
					elif self.__registrationStatus.text == "Conectando..":
						self.__registrationStatus.setText("Conectando...")
					elif self.__registrationStatus.text == "Conectando...":
						self.__registrationStatus.setText("Conectando")
				
				elif self.__registrationThread.getState() == 2:
					
					# Obtenemos la respuesta dada por el servidor
					result = self.__registrationThread.getResult()
					
					# Si el registro fue exitoso
					if result[11:15] == 'true':
						
						# Leemos el id retornado
						newUserId = result[23:43]
						
						# Si el nombre de usuario elegido ya existe
						if newUserId == "":
							self.__registrationStatus.setText("El Nombre de Usuario ya existe.")
							self.__registrationStatus.setPosition((835 - (self.__registrationStatus.getTextRenderLen() / 2), self.__registrationStatus.getPosition()[1]))
							
							# Se alista todo para una nueva conexion
							self.__registrationInProgress = False
							self.__registrationThread = None
							
						else:
							try:
								newFile = None
								
								# Creamos un archivo
								if olpcgames.ACTIVITY:  # Running as Activity
									name = os.getcwd() + '/UserInfo.txt'
									newFile = open(name, 'w+')
								else:
									newFile = open('UserInfo.txt', 'w+')
									
								# Volvemos a obtener los datos a persistir
								username = self.__textboxUsername.getText()
								password = self.__textboxPassword1.getText()
							
								# Escibimos el contenido apropiado
								newFile.write('''rootUserId:''' + newUserId + '''\n''')
								newFile.write('''username:''' + username + '''\n''')
								newFile.write('''password:''' + password + '''\n''')
								
								# Se cierra el archivo
								try:
									newFile.close
								except:
									pass
								
								# El registro fue exitoso, levantamos la bandera correspondiente
								self.__userCheck = True
								
								# Almacenamos la informacion en el juego
								Globals.INFO_ROOT_USER_ID = newUserId
								Globals.INFO_LEAF_USER_ID = 0
								Globals.INFO_USERNAME = username
								Globals.INFO_PASSWORD = password
								Globals.INFO_START_TIME = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
								
								# Informamos al usuario
								self.__registrationStatus.setText("Registro exitoso. Ingresando al juego...")
								self.__registrationStatus.setPosition((835 - (self.__registrationStatus.getTextRenderLen() / 2), self.__registrationStatus.getPosition()[1]))
								
								# Ya no se necesita la conexion abierta
								self.__registrationInProgress = False
								self.__registrationThread = None
								
							except:
								# Fue lanzada una excepcion relacionada con la apertura del archivo
								self.__registrationStatus.setText("Error en el Registro.")
								self.__registrationStatus.setPosition((835 - (self.__registrationStatus.getTextRenderLen() / 2), self.__registrationStatus.getPosition()[1]))
								
								# Se alista todo para una nueva conexion
								self.__registrationInProgress = False
								self.__registrationThread = None
								
								# Se cierra el archivo, sin importar lo que haya pasado
								try:
									newFile.close
								except:
									pass
								
					else:
						# Error en la respuesta del servidor
						self.__registrationStatus.setText("Error en el Registro.")
						self.__registrationStatus.setPosition((835 - (self.__registrationStatus.getTextRenderLen() / 2), self.__registrationStatus.getPosition()[1]))
						
						# Se alista todo para una nueva conexion
						self.__registrationInProgress = False
						self.__registrationThread = None
						
				elif self.__registrationThread.getState() == 3:
					
					# Falla de la conexion
					self.__registrationStatus.setText("Error de Conexión.")
					self.__registrationStatus.setPosition((835 - (self.__registrationStatus.getTextRenderLen() / 2), self.__registrationStatus.getPosition()[1]))
					
					# Se alista todo para una nueva conexion
					self.__registrationInProgress = False
					self.__registrationThread = None
					
		# Determinamos si hay un login en proceso
		elif self.__loginInProgress == True:
			
			# Si hay un hilo tratando de conectarse
			if self.__loginThread != None:
				
				if self.__loginThread.getState() == 1:
					
					if self.__loginStatus.text == "Conectando":
						self.__loginStatus.setText("Conectando.")
					elif self.__loginStatus.text == "Conectando.":
						self.__loginStatus.setText("Conectando..")
					elif self.__loginStatus.text == "Conectando..":
						self.__loginStatus.setText("Conectando...")
					elif self.__loginStatus.text == "Conectando...":
						self.__loginStatus.setText("Conectando")
				
				elif self.__loginThread.getState() == 2:
			   
					# Obtenemos la respuesta dada por el servidor
					result = self.__loginThread.getResult()
					
					# Si el login fue exitoso
					if result[11:15] == 'true':
						
						# Leemos el id retornado
						newUserId = result[23:43]
						
						# Si el nombre de usuario elegido no existe
						if newUserId == "":
							self.__loginStatus.setText("El Nombre de Usuario no existe.")
							
							# Se alista todo para una nueva conexion
							self.__loginInProgress = False
							self.__loginThread = None
							
						else:
							try:
								newFile = None
								
								# Creamos un archivo
								if olpcgames.ACTIVITY:  # Running as Activity
									name = os.getcwd() + '/UserInfo.txt'
									newFile = open(name, 'w+')
								else:
									newFile = open('UserInfo.txt', 'w+')
		
								# Volvemos a obtener los datos a persistir
								username = self.__textboxLoginUsername.getText()
								password = self.__textboxLoginPassword.getText()
							
								# Escibimos el contenido apropiado
								newFile.write('''rootUserId:''' + newUserId + '''\n''')
								newFile.write('''username:''' + username + '''\n''')
								newFile.write('''password:''' + password + '''\n''')
								
								# Se cierra el archivo
								try:
									newFile.close
								except:
									pass
								
								# El registro fue exitoso, levantamos la bandera correspondiente
								self.__userCheck = True
								
								# Almacenamos la informacion en el juego
								Globals.INFO_ROOT_USER_ID = newUserId
								Globals.INFO_LEAF_USER_ID = 0
								Globals.INFO_USERNAME = username
								Globals.INFO_PASSWORD = password
								Globals.INFO_START_TIME = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
								
								# Informamos al usuario
								self.__loginStatus.setText("Login exitoso. Ingresando al juego...")
								
								# Ya no se necesita la conexion abierta
								self.__loginInProgress = False
								self.__loginThread = None
								
							except:
								# Fue lanzada una excepcion relacionada con la apertura del archivo
								self.__loginStatus.setText("Error en el Login.")
								
								# Se alista todo para una nueva conexion
								self.__loginInProgress = False
								self.__loginThread = None
								
								# Se cierra el archivo, sin importar lo que haya pasado
								try:
									newFile.close
								except:
									pass
								
					else:
						# Error en la respuesta del servidor
						self.__loginStatus.setText("Error en el Login.")
						
						# Se alista todo para una nueva conexion
						self.__loginInProgress = False
						self.__loginThread = None
					  
				elif self.__loginThread.getState() == 3:
					
					self.__loginStatus.setText("Error de Conexión.")
					
					# Se alista todo para una nueva conexion
					self.__loginInProgress = False
					self.__loginThread = None
				
		# Detectamos todos los eventos y ejecutamos las acciones correspondientes
		if pygame.event:
			for event in pygame.event.get():
				 
				# Evento cerrar el juego
				if event.type == pygame.QUIT:
					Globals.thisGame.SetMode(10)
					
				# Deteccion de click de mouse
				elif event.type == pygame.MOUSEBUTTONDOWN:
					self.__doMouseAction(event)
					
				# Deteccion de teclas presionadas
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						Globals.thisGame.SetMode(10)
					elif event.key == pygame.K_RSHIFT:
						self.__switchCase()
					elif event.key == pygame.K_LSHIFT:
						self.__switchCase()
					else:
						self.__doKeyAction(event)
						
	def doPaint(self):
		
		# Background
		draw(self.background_Registration, (0, 0))

		# TextBox
		self.__textboxNames.doPaint()
		self.__textboxAge.doPaint()
		self.__textboxSchool.doPaint()
		self.__textboxGrade.doPaint()
		self.__textboxUsername.doPaint()
		self.__textboxPassword1.doPaint()
		self.__textboxPassword2.doPaint()
		self.__textboxLoginUsername.doPaint()
		self.__textboxLoginPassword.doPaint()

		# Buttons with Hover
		if self.__registrationInProgress == False:
			if self.__hoverRegistration == True:
				draw(self.input_Registration_On, (670, 475))
			else:
				draw(self.input_Registration_Off, (670, 475))
		else:
			draw(self.input_Connecting, (670, 475))
			
		if self.__loginInProgress == False:
			if self.__hoverLoginButton == True:
				draw(self.input_Login_On, (435, 750))
			else:
				draw(self.input_Login_Off, (435, 750))
		else:
			draw(self.input_Connecting, (435, 750))

		# Connecton Status
		self.__registrationStatus.doPaint()
		self.__loginStatus.doPaint()
		
		if self.__hoverCloseGame == True:
			draw(self.input_CloseGame_On, (1200 - 87, 0))
		else:
			draw(self.input_CloseGame_Off, (1200 - 87, 0))
		
	def __doKeyAction(self, event):
		
		# Si no hay algun evento en progreso...
		if (self.__registrationInProgress == False) and (self.__loginInProgress == False) and (self.__userCheck == False):
			
			self.__textboxNames.doKeyAction(event)
			self.__textboxAge.doKeyAction(event)
			self.__textboxSchool.doKeyAction(event)
			self.__textboxGrade.doKeyAction(event)
			self.__textboxUsername.doKeyAction(event)
			self.__textboxPassword1.doKeyAction(event)
			self.__textboxPassword2.doKeyAction(event)
			self.__textboxLoginUsername.doKeyAction(event)
			self.__textboxLoginPassword.doKeyAction(event)
		
	def __doMouseAction(self, event):
		
		if self.__userCheck == False:
		
			# Removemos el foco de todas la cajas de texto
			self.__textboxNames.quitFocus()
			self.__textboxAge.quitFocus()
			self.__textboxSchool.quitFocus()
			self.__textboxGrade.quitFocus()
			self.__textboxUsername.quitFocus()
			self.__textboxPassword1.quitFocus()
			self.__textboxPassword2.quitFocus()
			self.__textboxLoginUsername.quitFocus()
			self.__textboxLoginPassword.quitFocus()
			
			# Detectamos la posicion en X y Y del click
			xPos, yPos = event.pos
	
			# Close Game
			if (xPos >= 1200 - 87) and (xPos <= 1200) and (yPos >= 0) and (yPos <= 0 + 74):
				Globals.thisGame.SetMode(10)
			
			# Registration Button
			elif (xPos >= 670) and (xPos <= 670 + 330) and (yPos >= 475) and (yPos <= 475 + 65):
				
				if self.__registrationInProgress == False:
				
					# Desabilitamos el registro
					self.__registrationInProgress = True
					
					# Reiniciamos esta bandera dado que un nuevo proceso de verificacion de usuario va a comenzar
					self.__userCheck = False
					
					# Reiniciamos los mensajes e estado
					self.__loginStatus.setText("")
					self.__registrationStatus.setText("")
					
					# Verificamos los datos a enviar
					names = self.__textboxNames.getText()
					age = self.__textboxAge.getText()
					school = self.__textboxSchool.getText()
					grade = self.__textboxGrade.getText()
					username = self.__textboxUsername.getText()
					password1 = self.__textboxPassword1.getText()
					password2 = self.__textboxPassword2.getText()
					
					# Verificamos si todos los datos fueron ingresados
					if (names == "") or (age == "") or (school == "") or (grade == "") or (username == "") or (password1 == "") or (password2 == ""):
	
						self.__registrationStatus.setText("Se deben llenar todos los campos.")
						self.__registrationStatus.setPosition((835 - (self.__registrationStatus.getTextRenderLen() / 2), self.__registrationStatus.getPosition()[1]))
						
						# Se alista todo para una nueva conexion
						self.__registrationInProgress = False
						self.__registrationThread = None
						return
									
					# Verificamos si las contraseñas coinciden
					if password1 != password2:
						
						self.__registrationStatus.setText("Las contraseñas no coinciden.")
						self.__registrationStatus.setPosition((835 - (self.__registrationStatus.getTextRenderLen() / 2), self.__registrationStatus.getPosition()[1]))
						
						# Se alista todo para una nueva conexion
						self.__registrationInProgress = False
						self.__registrationThread = None
						return
					
					try:
						self.__registrationStatus.setText("Conectando...")
						self.__registrationStatus.setPosition((835 - (self.__registrationStatus.getTextRenderLen() / 2), self.__registrationStatus.getPosition()[1]))
					
						# Parametros de conexion
						url = 'http://www.transformando.gov.co/api/public/index/register'
						jsonParameters = '''
						{
							"gameId": "2",
							"newUser": {
								"name": "''' + names + '''",
								"nickname": "''' + username + '''",
								"password": "''' + password1 + '''",
								"age": "''' + age + '''",
								"school": "''' + school + '''",
								"degree": "''' + grade + '''"
							}
						}'''
						parameters = urllib.urlencode({'data': jsonParameters})
						
						# Hacemos la solicitud por POST
						self.__registrationThread = ConnectionController(1, url, parameters)
						self.__registrationThread.start()
						
					except:
						self.__registrationStatus.setText("Error de Conexión.")
						self.__registrationStatus.setPosition((835 - (self.__registrationStatus.getTextRenderLen() / 2), self.__registrationStatus.getPosition()[1]))
						
						# Se alista todo para una nueva conexion
						self.__registrationInProgress = False
						self.__registrationThread = None
			
			# Login Button
			elif (xPos >= 435) and (xPos <= 435 + 330) and (yPos >= 750) and (yPos <= 750 + 65):
		
				if self.__loginInProgress == False:
				
					# Desabilitamos el registro
					self.__loginInProgress = True
					
					# Reiniciamos esta bandera dado que un nuevo proceso de verificacion de usuario va a comenzar
					self.__userCheck = False
					
					# Reiniciamos los mensajes e estado
					self.__loginStatus.setText("")
					self.__registrationStatus.setText("")
					
					# Verificamos los datos a enviar
					username = self.__textboxLoginUsername.getText()
					password = self.__textboxLoginPassword.getText()
					
					# Verificamos si todos los datos fueron ingresados
					if (username == "") or (password == ""):
	
						self.__loginStatus.setText("Se deben llenar todos los campos.")
						
						# Se alista todo para una nueva conexion
						self.__loginInProgress = False
						self.__loginThread = None
						return
									
					try:
						self.__loginStatus.setText("Conectando...")
					
						# Parametros de conexion
						url = 'http://www.transformando.gov.co/api/public/index/checkuser'
						parameters = urllib.urlencode({'user': username, 'pass': password})
						
						# Hacemos la solicitud por POST
						self.__loginThread = ConnectionController(1, url, parameters)
						self.__loginThread.start()
						
					except:
						self.__loginStatus.setText("Error de Conexión.")
						
						# Se alista todo para una nueva conexion
						self.__loginInProgress = False
						self.__loginThread = None
			
			# Textbox
			else:
				self.__textboxNames.doMouseAction(event)
				self.__textboxAge.doMouseAction(event)
				self.__textboxSchool.doMouseAction(event)
				self.__textboxGrade.doMouseAction(event)
				self.__textboxUsername.doMouseAction(event)
				self.__textboxPassword1.doMouseAction(event)
				self.__textboxPassword2.doMouseAction(event)
				self.__textboxLoginUsername.doMouseAction(event)
				self.__textboxLoginPassword.doMouseAction(event)
		
	def __switchCase(self):
		if self.__userCheck == False:
			self.__textboxNames.switchCase()
			self.__textboxAge.switchCase()
			self.__textboxSchool.switchCase()
			self.__textboxGrade.switchCase()
			self.__textboxUsername.switchCase()
			self.__textboxPassword1.switchCase()
			self.__textboxPassword2.switchCase()
			self.__textboxLoginUsername.switchCase()
			self.__textboxLoginPassword.switchCase()

class ConnectionController(threading.Thread):
	
	def __init__(self, method, url, parameters):
		threading.Thread.__init__(self)
		self.__method = method
		self.__url = url
		self.__parameters = parameters
		self.__state = None
		self.__result = None
  
	def run(self):
		
		# Comienza el proceso de conexion
		self.__state = 1
		
		# Hacemos la solicitud por POST
		if self.__method == 1:
			
			try:
				self.__result = urllib.urlopen(self.__url, self.__parameters).read()
				self.__state = 2
			except: 
				self.__state = 3
			
	def getResult(self):
		return self.__result
		
	def getState(self):        
		return self.__state

def main():
		pygame.init()
		game = Juego()
		game.run();

if __name__ == '__main__':
	main()