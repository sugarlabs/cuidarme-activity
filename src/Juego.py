# -*- coding: utf-8 -*-

import pygame
import sys
import random
import Globals
from src.Pacman import Pacman
from src.game import game
from pygame.locals import *
from threading import Timer
import gc
gc.enable()


class Juego():

    def __init__(self):
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
        self.dyingPos = (0, 0)
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

        # Control
        self.__dataProcessDefined = False
        self.__dataSentDefined = False

        self.__sendBatchThread = None
        self.__sendBatchInProgress = False

        self.window = pygame.display.set_mode((1200, 825), 0, 0)
        pygame.display.set_caption("Cuidarme")

        Globals.screen = pygame.display.get_surface()

        Globals.img_Background = pygame.image.load(
            "res/backgrounds/Splash_1.png").convert()

        pygame.mixer.init()

        Globals.snd_item = pygame.mixer.Sound("res/sounds/FX/recojeitem2.ogg")
        Globals.snd_timeOver = pygame.mixer.Sound(
            "res/sounds/FX/fanfarria_error.ogg")
        Globals.snd_good = pygame.mixer.Sound("res/sounds/FX/saleitem.ogg")
        self.explosion = pygame.mixer.Sound("res/sounds/FX/explosion.ogg")
        self.errorSound = pygame.mixer.Sound("res/sounds/FX/error.ogg")
        pygame.mixer.music.load('res/sounds/Musica/splash.ogg')

        self.btn_a1 = pygame.image.load(
            "res/sprite/AnswerA_Off.png").convert_alpha()
        self.btn_b1 = pygame.image.load(
            "res/sprite/AnswerB_Off.png").convert_alpha()
        self.btn_c1 = pygame.image.load(
            "res/sprite/AnswerC_Off.png").convert_alpha()
        # self.__backgroundTransparent = pygame.image.load("res/backgrounds/0.png").convert()
        self.backgroundQuestion = pygame.image.load(
            "res/backgrounds/Question.png").convert_alpha()
        self.game_StarBig_On = pygame.image.load(
            "res/sprite/StarBig_On.png").convert_alpha()
        self.ghostNormalFrame = pygame.image.load(
            "res/sprite/ghost2.png").convert_alpha()
        self.ghostVulnerableFrame = pygame.image.load(
            "res/sprite/ghost2_v.png").convert_alpha()
        self.clockBack = pygame.image.load(
            "res/sprite/clockBack.png").convert_alpha()
        self.clockImg = pygame.image.load(
            "res/sprite/ClockBig.png").convert_alpha()
        self.timeOverImg = pygame.image.load(
            "res/sprite/timeOver.png").convert_alpha()
        self.tryAgainImg = pygame.image.load(
            "res/sprite/MessageTryAgain.png").convert_alpha()
        self.winImg = pygame.image.load(
            "res/sprite/mensaje_felicidades.png").convert_alpha()
        self.popup = pygame.image.load(
            "res/backgrounds/fondo_caritas.png").convert_alpha()
        self.buttonUp = pygame.image.load(
            "res/sprite/boton_normal.png").convert_alpha()
        self.buttonDown = pygame.image.load(
            "res/sprite/boton_presionado.png").convert_alpha()
        self.buttonstate = self.buttonUp
        self.fondoItem = pygame.image.load(
            "res/sprite/fondoItem.png").convert_alpha()
        self.starIcon = pygame.image.load(
            "res/tiles/star2.png").convert_alpha()

        self.inst1 = pygame.image.load(
            "res/sprite/cambiar.png").convert_alpha()
        self.inst2 = pygame.image.load(
            "res/sprite/seleccionar.png").convert_alpha()

        self.__collectedItemsIndicator = Text(
            None, 30, 'x 0', (255, 255, 255), 55, 5)
        self.__timeRemainingIndicator = Text(
            None, 30, '5:00', (255, 255, 255), 610, 5)
        self.instructions = Text(
            None, 15, 'Selecciona la emoción que', (255, 0, 255), 105, 160)
        self.instructions1 = Text(
            None, 15, 'coincida con la descripción', (255, 0, 255), 105, 200)

    def showDialog(self):
        # Muestra la interfaz de preguntas
        draw(self.backgroundQuestion, (0, 0))
        draw(self.game_StarBig_On, (250 + (130 * 0), 125))
        draw(self.game_StarBig_On, (250 + (130 * 1), 125))
        draw(self.game_StarBig_On, (250 + (130 * 2), 125))
        draw(self.game_StarBig_On, (250 + (130 * 3), 125))
        draw(self.game_StarBig_On, (250 + (130 * 4), 125))
        paintMultiline(80, 370, Globals.questions[Globals.questionId])
        draw(self.btn_a1, (90, 500))
        draw(self.btn_b1, (90, 580))
        draw(self.btn_c1, (90, 660))
        paintMultiline(180, 502, Globals.answers[Globals.questionId][0][0])
        paintMultiline(180, 582, Globals.answers[Globals.questionId][1][0])
        paintMultiline(180, 662, Globals.answers[Globals.questionId][2][0])

        if pygame.key.get_pressed()[
                pygame.K_KP7] or pygame.key.get_pressed()[
                pygame.K_a]:
            self.checkAnswer(0)
        elif pygame.key.get_pressed()[pygame.K_KP3] or pygame.key.get_pressed()[pygame.K_b]:
            self.checkAnswer(1)
        elif pygame.key.get_pressed()[pygame.K_KP1] or pygame.key.get_pressed()[pygame.K_c]:
            self.checkAnswer(2)

    def checkAnswer(self, value):
        if (Globals.answers[Globals.questionId][value][1] == 1):
            # respuesta correcta
            self.dyingPos = (
                Globals.ghosts[Globals.questionId].x + 25, Globals.ghosts[Globals.questionId].y)
            del Globals.ghosts[Globals.questionId]
            self.dialog = 0
            Globals.thisGame.AddToScore(25)
            self.ghostDying = 1
            self.explosion.play()
            self.turnNormal()
            self.checkCompletion()
        else:
            # respuesta incorrecta
            self.dialog = 0
            self.tryAgain = 1
            self.restartPlayer()
        pygame.mixer.music.load(Globals.actualMusic)
        pygame.mixer.music.play(-1)

    def checkCompletion(self):
        if len(
                Globals.thisLevel.items) < 1 and len(
                Globals.ghosts.items()) < 1:
            # if len(Globals.ghosts.items()) < 1:
            Globals.ghosts = {}
            Globals.thisGame.SetMode(6)

    def showEmotionTrivia(self):
        draw(self.popup, (13, 30))
        draw(self.buttonstate, (530, 535))
        self.instructions.doPaint()
        self.instructions1.doPaint()
        paintMultiline(105, 240, Globals.emotion[0])
        thisface = pygame.image.load('res/sprite/' +
                                     Globals.selectedCharacter +
                                     '_em' +
                                     str(self.emotionSelected) +
                                     '.png')
        drawScaled(thisface, (240, 351), (840, 170))
        del thisface
        drawScaled(self.inst1, (268, 80), (280, 745))
        drawScaled(self.inst2, (268, 80), (610, 745))
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
                    if self.emotionSelected == Globals.emotion[1]:
                        Globals.thisGame.SetMode(7)
                    else:
                        self.errorSound.play()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            Globals.thisGame.SetMode(10)

    def CheckInputs(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                Globals.thisGame.SetMode(10)

        if Globals.thisGame.mode == 1 and self.dialog == 0:
            if pygame.key.get_pressed()[
                    pygame.K_KP6] or pygame.key.get_pressed()[
                    pygame.K_RIGHT]:
                Globals.player.velX = Globals.player.speed
                Globals.player.velY = 0

            elif pygame.key.get_pressed()[pygame.K_KP4] or pygame.key.get_pressed()[pygame.K_LEFT]:
                Globals.player.velX = -Globals.player.speed
                Globals.player.velY = 0

            elif pygame.key.get_pressed()[pygame.K_KP2] or pygame.key.get_pressed()[pygame.K_DOWN]:
                Globals.player.velX = 0
                Globals.player.velY = Globals.player.speed

            elif pygame.key.get_pressed()[pygame.K_KP8] or pygame.key.get_pressed()[pygame.K_UP]:
                Globals.player.velX = 0
                Globals.player.velY = -Globals.player.speed

            else:
                Globals.player.velX = 0
                Globals.player.velY = 0

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
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
        self.timeOver = 1
        Globals.thisGame.modeTimer = 0
        Globals.thisGame.SetMode(4)

    def turnNormal(self):
        Globals.player.state = 1
        Globals.player.speed = Globals.playerSpeed
        for k, item in Globals.ghosts.items():
            item.anim[2] = self.ghostNormalFrame

    def turnVulnerable(self):
        Globals.player.state = 2
        Globals.player.speed = Globals.playerSpeed + 3
        for k, item in Globals.ghosts.items():
            item.anim[2] = self.ghostVulnerableFrame

    def restorePowerups(self):
        for item in Globals.thisLevel.powerups:
            item[4] = 1

    def getRemainingTime(self):
        _tim = int(Globals.thisGame.timer / 30)
        _tim = 480 - _tim
        _mins = int(_tim / 60)
        _secs = _tim % 60
        _strsecs = str(_secs)
        if _secs < 10:
            _strsecs = '0' + str(_secs)
        return str(_mins) + ':' + _strsecs

    def drawPowerups(self):
        for item in Globals.thisLevel.powerups:
            if (item[4] == 1):
                draw(
                    self.starIcon,
                    (item[0] -
                     Globals.thisGame.screenPixelPos[0],
                     item[2] -
                        Globals.thisGame.screenPixelPos[1]))
    #      _____________________________________________

    def goNextLevel(self):
        Globals.thisLevel = Level()
        if Globals.thisGame.levelNum == 1:
            Globals.thisGame.levelNum = random.randint(2, 10)
        else:
            Globals.thisGame.levelNum = random.randint(1, 10)
            Globals.playerSpeed = 18
            Globals.ghostSpeed = 18
            Globals.player.speed = Globals.playerSpeed
        Globals.INFO_STARS += Globals.thisGame.score
        Globals.thisGame.StartNewGame(Globals.thisGame.levelNum)
        Globals.thisLevel.LoadLevel(Globals.thisGame.levelNum)
        Globals.player.velX = 0
        Globals.player.velY = 0
        Globals.player.anim_pacmanCurrent = Globals.player.anim_pacmanS
        gc.collect()

    def launch(self):
        Globals.player = Pacman()
        # create game and level objects and load first level
        Globals.thisGame = game()
        Globals.thisLevel = Level()
        Globals.thisLevel.LoadLevel(Globals.thisGame.GetLevelNum())
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(-1)

        self.ghostDieAnim = {}
        for i in range(1, 11, 1):
            self.ghostDieAnim[i] = pygame.image.load(
                "res/sprite/exp" + str(i) + ".png").convert_alpha()

        # self.window = pygame.display.set_mode( Globals.thisGame.screenSize, SWSURFACE  )
        # self.window = pygame.display.set_mode( (1200,825), 0 ,0 )
        self.window.set_alpha(None)

        while True:

            # --------- Background
            # --------------------------------------------------------------

            if Globals.thisGame.mode == 1:
                back_x = 0
                back_y = 0
                if (Globals.thisLevel.levelSize -
                        Globals.thisGame.screenPixelPos[0]) < Globals.thisLevel.levelOffset:
                    back_x = -Globals.thisLevel.levelOffset
                else:
                    back_x = -Globals.thisGame.screenPixelPos[0]
                if (Globals.thisLevel.levelHeight -
                        Globals.thisGame.screenPixelPos[1]) < Globals.thisLevel.heightOffset:
                    back_y = -Globals.thisLevel.heightOffset
                else:
                    back_y = -Globals.thisGame.screenPixelPos[1]

                draw(Globals.img_Background, (back_x, back_y))
                # normal gameplay mode
                self.CheckInputs()
                if not self.dialog:
                    Globals.player.Move()
                    for item in Globals.thisLevel.items:
                        if Globals.thisLevel.CheckIfHit(
                                (Globals.player.x, Globals.player.y), (item[0], item[2]), (25, 21)):
                            Globals.thisLevel.items.remove(item)
                            Globals.thisGame.AddToScore(1)
                            Globals.snd_item.play()
                            self.checkCompletion()
                            break
                    for item in Globals.thisLevel.powerups:
                        if Globals.thisLevel.CheckIfHit(
                                (Globals.player.x, Globals.player.y), (item[0], item[2]), (50, 41)) and not item[4] == 0:
                            item[4] = 0
                            mytimer = Timer(10.0, self.turnNormal)
                            mytimer.start()
                            self.PUtimer = 1
                            self.turnVulnerable()
                            break
                    for k, item in Globals.ghosts.items():
                        if Globals.thisLevel.CheckIfHit(
                                (Globals.player.x, Globals.player.y), (item.x, item.y), (50, 90)):
                            if Globals.player.state == 2:
                                Globals.questionId = item.id
                                self.dialog = 1
                                pygame.mixer.music.load(
                                    'res/sounds/Musica/preguntas.ogg')
                                pygame.mixer.music.play(-1)
                                Globals.player.velX = 0
                                Globals.player.velY = 0
                            elif Globals.player.state == 1:
                                Globals.thisGame.AddToScore(-15)
                                if Globals.thisGame.score < 0:
                                    self.gameOver()
                                else:
                                    Globals.thisLevel.Restart()
                                    self.tryAgain = 1
                    Globals.player.Draw()
                    for k, item in Globals.ghosts.items():
                        item.Move()
                    if self.PUtimer > 0:
                        self.PUtimer += 1
                        if (self.PUtimer == 450):
                            self.restorePowerups()
                    if self.ghostDying:
                        draw(self.ghostDieAnim[self.ghostDieFrame],
                             (self.dyingPos[0] - Globals.thisGame.screenPixelPos[0],
                              self.dyingPos[1] - Globals.thisGame.screenPixelPos[1]))
                        self.ghostAnimTimer += 1
                        if self.ghostAnimTimer == 4:
                            self.ghostDieFrame += 1
                            self.ghostAnimTimer = 1
                        if self.ghostDieFrame == 11:
                            self.ghostDieFrame = 1
                            self.ghostDying = 0

            elif Globals.thisGame.mode == 3:
                self.CheckInputs()
                # self.checkPersistence()
                # Globals.thisGame.StartNewGame()
                Globals.thisGame.modeTimer += 1
                if Globals.thisGame.modeTimer == 1:
                    pass
                    # self.checkPersistence()
                elif Globals.thisGame.modeTimer == 30:
                    Globals.img_Background = pygame.image.load(
                        "res/backgrounds/Splash_2.png")
                elif Globals.thisGame.modeTimer == 60:
                    Globals.img_Background = pygame.image.load(
                        "res/backgrounds/Splash_3.png")
                elif Globals.thisGame.modeTimer == 90:
                    Globals.img_Background = pygame.image.load(
                        "res/backgrounds/Splash_4.png")
                elif Globals.thisGame.modeTimer == 120:
                    Globals.img_Background = pygame.image.load(
                        "res/backgrounds/Splash_5.png")
                elif Globals.thisGame.modeTimer >= 150:
                    # if self.persistenceChecked:
                        # self.showScreen(self.screenToGo)
                    # Globals.thisGame.StartNewGame(1)
                    Globals.thisGame.SetMode(9)
                draw(Globals.img_Background, (0, 0))

            elif Globals.thisGame.mode == 4:
                if self.timeOver:
                    draw(self.timeOverImg, (229, 264))
                Globals.thisGame.modeTimer += 1
                if Globals.thisGame.modeTimer == 150:
                    Globals.thisGame.changeToLevel(1)

            elif Globals.thisGame.mode == 6:
                # Globals.thisGame.SetMode(7)
                self.showEmotionTrivia()

            elif Globals.thisGame.mode == 7:
                Globals.thisGame.modeTimer += 1
                draw(self.winImg, (111, 25))
                if Globals.thisGame.modeTimer == 100:
                    self.goNextLevel()

            elif Globals.thisGame.mode == 8:
                # blank screen before changing levels
                Globals.thisGame.modeTimer += 1
                if Globals.thisGame.modeTimer == 10:
                    self.goNextLevel()
                    # Globals.thisGame.SetNextLevel()
            elif Globals.thisGame.mode == 9:
                if Globals.thisGame.modeTimer == 0:
                    back = pygame.image.load(
                        "res/backgrounds/tutorial.png").convert()
                    Globals.thisGame.modeTimer += 1
                draw(back, (0, 0))
                for event in pygame.event.get():
                    if event.type == QUIT:
                        Globals.thisGame.SetMode(10)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_KP1 or event.key == pygame.K_RETURN:
                            Globals.thisGame.SetMode(2)
            elif Globals.thisGame.mode == 2:
                if Globals.thisGame.modeTimer == 0:
                    back = pygame.image.load(
                        "res/backgrounds/select_gender.png").convert()
                    gm1 = pygame.image.load(
                        "res/sprite/select_gender_m1.png").convert_alpha()
                    gm2 = pygame.image.load(
                        "res/sprite/select_gender_m2.png").convert_alpha()
                    gw1 = pygame.image.load(
                        "res/sprite/select_gender_w1.png").convert_alpha()
                    gw2 = pygame.image.load(
                        "res/sprite/select_gender_w2.png").convert_alpha()
                    Globals.thisGame.modeTimer += 1
                draw(back, (0, 0))
                if Globals.selectedCharacter == 'm':
                    draw(gm1, (204, 88))
                    draw(gw2, (561, 88))
                else:
                    draw(gm2, (204, 88))
                    draw(gw1, (561, 88))
                drawScaled(self.inst1, (268, 80), (280, 745))
                drawScaled(self.inst2, (268, 80), (610, 745))

                for event in pygame.event.get():
                    if event.type == QUIT:
                        Globals.thisGame.SetMode(10)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_KP6 or event.key == pygame.K_RIGHT:
                            Globals.selectedCharacter = 'w'
                        elif event.key == pygame.K_KP4 or event.key == pygame.K_LEFT:
                            Globals.selectedCharacter = 'm'
                        elif event.key == pygame.K_KP1 or event.key == pygame.K_RETURN:
                            Globals.player = Pacman()
                            Globals.thisGame.modeTimer = 0
                            Globals.thisGame.StartNewGame(1)

            elif Globals.thisGame.mode == 10:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pass
                if Globals.thisGame.modeTimer == 0:
                    Globals.img_Background = pygame.image.load(
                        "res/backgrounds/Splash_final.png")
                    draw(Globals.img_Background, (0, 0))
                    # self.savePersistence()
                if Globals.thisGame.modeTimer == 150:
                    sys.exit(0)

            elif Globals.thisGame.mode == 11:
                Globals.thisGame.SetMode(9)

            if not Globals.thisGame.mode == 8:
                # Globals.thisLevel.DrawMap()
                if Globals.thisGame.mode == 1:
                    Globals.thisGame.SmartMoveScreen()
                    Globals.thisLevel.drawItems()
                    self.drawPowerups()
                    for k, item in Globals.ghosts.items():
                        item.Draw()

                    if self.dialog:
                        self.showDialog()
                    if self.tryAgain:
                        draw(self.tryAgainImg, (229, 250))
                        self.tryAgainTimer += 1
                        if self.tryAgainTimer == 60:
                            self.tryAgain = 0
                            self.tryAgainTimer = 0

                    # indicadores de items, siempre deben ir de ultimo
                    draw(self.fondoItem, (0, 0))
                    draw(self.starIcon, (5, 10))
                    self.__collectedItemsIndicator.setText(
                        'x ' + str(Globals.thisGame.score))
                    self.__collectedItemsIndicator.doPaint()
                    draw(self.clockBack, (495, 0))
                    draw(self.clockImg, (500, 3))
                    self.__timeRemainingIndicator.setText(
                        self.getRemainingTime())
                    self.__timeRemainingIndicator.doPaint()
                    Globals.thisGame.timer += 1
                    if Globals.thisGame.timer == 17550:
                        pygame.mixer.music.load("res/sounds/FX/reloj.ogg")
                        pygame.mixer.music.play(-1)
                    if Globals.thisGame.timer == 18000:
                        pygame.mixer.music.stop()
                        self.gameOver()
            pygame.display.update()
            self.clock.tick(30)


class Text:
    def __init__(self, fontName, size, text, color, lx, ly):
        self.__font = pygame.font.Font('res/BorisBlackBloxx.ttf', 35)
        self.__text = text
        self.__color = color
        self.__positionX = lx
        self.__positionY = ly

    def doPaint(self):
        text = unicode(self.__text, "UTF-8")
        draw(self.__font.render(text, 1, self.__color),
             (self.__positionX, self.__positionY))

    def setText(self, newText):
        self.__text = newText


class ghost():
    def __init__(self, ghostID):
        self.x = 0
        self.y = 0
        self.velX = 0
        self.velY = 0
        self.speed = Globals.ghostSpeed
        self.nearestRow = 0
        self.nearestCol = 0
        self.id = ghostID
        self.timer = 0
        # ghost "state" variable
        # 1 = normal
        # 2 = vulnerable
        # 3 = spectacles
        self.homeX = 0
        self.homeY = 0
        self.currentPath = "L"
        self.anim = {}
        for i in range(1, 5, 1):
            self.anim[i] = pygame.image.load(
                "res/sprite/ghost" + str(i) + ".png")
        self.animFrame = 1
        self.animDelay = 0

    def Draw(self):
        if Globals.thisGame.mode == 3:
            return False

        Globals.screen.blit(self.anim[self.animFrame],
                            (self.x - Globals.thisGame.screenPixelPos[0],
                             self.y - Globals.thisGame.screenPixelPos[1]))

        if Globals.thisGame.mode == 6 or Globals.thisGame.mode == 7:
            # don't animate ghost if the level is complete
            return False

        self.animDelay += 1

        if self.animDelay == 2:
            self.animFrame += 1

            if self.animFrame == 5:
                # wrap to beginning
                self.animFrame = 1

            self.animDelay = 0

    def Move(self):
        self.nearestRow = int(((self.y + 50) / 25))
        self.nearestCol = int(((self.x + 25) / 25))
        if not Globals.thisLevel.CheckIfHitWall(
            (self.x +
             self.velX,
             self.y +
             self.velY),
            (50,
             100)) and not Globals.thisLevel.CheckIfHit(
            (Globals.player.x +
             Globals.player.velX,
             Globals.player.y +
             Globals.player.velY),
            (self.x +
             self.velX,
             self.y +
             self.velY),
            (50,
             100)):
            self.x += self.velX
            self.y += self.velY
            self.timer += 1
            if (self.timer >= 60):
                self.getRandomWay()
                self.timer = 0
        else:
            self.getRandomWay()

    def getRandomWay(self):
        ran = random.randint(0, 4)
        if ran == 0:
            self.currentPath = 'L'
            (self.velX, self.velY) = (-self.speed, 0)
        elif ran == 1:
            self.currentPath = 'U'
            (self.velX, self.velY) = (0, -self.speed)
        elif ran == 2:
            self.currentPath = 'R'
            (self.velX, self.velY) = (self.speed, 0)
        elif ran == 3:
            self.currentPath = 'D'
            (self.velX, self.velY) = (0, self.speed)


def draw(target, xxx_todo_changeme8):
    (x, y) = xxx_todo_changeme8
    Globals.screen.blit(target, (x, y))


def drawScaled(target, xxx_todo_changeme9, xxx_todo_changeme10):
    (w, h) = xxx_todo_changeme9
    (x, y) = xxx_todo_changeme10
    item = pygame.transform.scale(target, (w, h))
    Globals.screen.blit(item, (x, y))


def paintMultiline(left, top, texts):
    for et in texts:
        line = Text(None, 40, et, (255, 255, 255), left, top)
        line.doPaint()
        top += 33


class Label:

    def __init__(self, text, size, color, positionXY):
        self.text = text
        self.__font = pygame.font.Font('res/BorisBlackBloxx.ttf', size)
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

    def __init__(
            self,
            posX,
            posY,
            width,
            maxChars,
            font,
            isPassword,
            displaySurface):
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
        if self.__focus:
            pygame.draw.rect(self.displaySurface,
                             self.__focusBorderColor,
                             pygame.Rect(self.__posX - self.__focusBorderWidth,
                                         self.__posY - self.__focusBorderWidth,
                                         self.__width + (self.__focusBorderWidth * 2),
                                         self.__height + (self.__focusBorderWidth * 2)))

        # Borde
        pygame.draw.rect(self.displaySurface,
                         self.__normalBorderColor,
                         pygame.Rect(self.__posX - self.__normalBorderWidth,
                                     self.__posY - self.__normalBorderWidth,
                                     self.__width + (self.__normalBorderWidth * 2),
                                     self.__height + (self.__normalBorderWidth * 2)))

        # Contenido
        pygame.draw.rect(
            self.displaySurface,
            self.__contentColor,
            pygame.Rect(
                self.__posX,
                self.__posY,
                self.__width,
                self.__height))

        # Texto ingresado
        if not self.__isPassword:
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

        if (
                xPos >= self.__posX) and (
                xPos <= self.__posX +
                self.__width) and (
                yPos >= self.__posY) and (
                    yPos <= self.__posY +
                self.__height):
            self.__focus = True
        else:
            self.__focus = False

    def doKeyAction(self, event):
        if self.__focus:

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
                if self.__uppercase:
                    charToAdd = charToAdd.upper()
                    # self.__uppercase = False

                # Añadimos la letra a la cadena
                self.__textReal.addChar(charToAdd)
                self.__textPassword.addChar("*")

    def switchCase(self):
        if self.__uppercase:
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
        self.thisFruit = None
        self.pellets = 0
        self.levelNum = 0

    def SetMapTile(self, xxx_todo_changeme, newValue):
        (row, col) = xxx_todo_changeme
        self.map[(row * self.lvlWidth) + col] = newValue

    def GetMapTile(self, xxx_todo_changeme1):
        (row, col) = xxx_todo_changeme1
        if row >= 0 and row < self.lvlHeight and col >= 0 and col < self.lvlWidth:
            return self.map[(row * self.lvlWidth) + col]
        else:
            return 0

    def getItem(self, row, col):
        for item in range(0, len(self.items), 1):
            if (self.items[item][0] == col and self.items[item][1] == row):
                return item

    def IsWall(self, xxx_todo_changeme2):
        (row, col) = xxx_todo_changeme2
        if row > self.lvlHeight - 1 or row < 0:
            return True
        if col > self.lvlWidth - 1 or col < 0:
            return True
        result = self.GetMapTile((row, col))
        if result == 1:
            return True
        else:
            return False

    def CheckIfHitWall(self, xxx_todo_changeme3, xxx_todo_changeme4):
        (possibleX, possibleY) = xxx_todo_changeme3
        (width, height) = xxx_todo_changeme4
        numCollisions = 0
        ppr = possibleX + width
        ppb = possibleY + height
        leftCol = int(possibleX / 25)
        rightCol = int(ppr / 25) + 1
        topRow = int(possibleY / 25)
        bottomRow = int(ppb / 25) + 1
        for iRow in range(topRow, bottomRow, 1):
            for iCol in range(leftCol, rightCol, 1):
                if (possibleX - (iCol * 25) < 25) and (ppr - (iCol * 25) > - \
                    25) and (possibleY - (iRow * 25) < 25) and (ppb - (iRow * 25) > -25):
                    if self.IsWall((iRow, iCol)):
                        numCollisions += 1
        if numCollisions > 0:
            return True
        else:
            return False

    def CheckIfHit(
            self,
            xxx_todo_changeme5,
            xxx_todo_changeme6,
            xxx_todo_changeme7):
        (playerX, playerY) = xxx_todo_changeme5
        (x, y) = xxx_todo_changeme6
        (w, h) = xxx_todo_changeme7
        ppr = playerX + 56
        ppb = playerY + 99
        rl = x + w
        dl = y + h
        if (((playerX <= x and ppr > x) or (ppr >= rl and playerX < rl) or (playerX <= x and ppr > rl)) and (
                (playerY <= y and ppb > dl) or (playerY >= y and playerY < dl) or (playerY <= y and ppb > y))):
            return True
        else:
            return False

    def DrawMap(self):
        for row in range(-1, Globals.thisGame.tilesY + 1, 1):
            outputLine = ""
            for col in range(-1, Globals.thisGame.tilesX + 1, 1):
                actualRow = Globals.thisGame.screenNearestTilePos[0] + row
                actualCol = Globals.thisGame.screenNearestTilePos[1] + col
                useTile = self.GetMapTile((actualRow, actualCol))
                if useTile == 2:
                    Globals.screen.blit(
                        Globals.tileIDImage[useTile],
                        (col * 25 - Globals.thisGame.screenPixelOffset[0],
                         row * 25 - Globals.thisGame.screenPixelOffset[1]))

    def drawItems(self):
        for i in range(0, len(self.items), 1):
            _x = self.items[i][0] - Globals.thisGame.screenPixelPos[0]
            _y = self.items[i][2] - Globals.thisGame.screenPixelPos[1]
            if _x > 0 and _x < 1200 and _y > 0 and _y < 825:
                draw(self.thisFruit, (_x, _y))

    def LoadLevel(self, levelNum):
        self.map = {}
        self.actions = []
        Globals.thisGame.timer = 0
        f = open("res/levels/" + str(levelNum) + ".csv", 'r')
        randinfo = random.randint(1, 10)
        Globals.questions = eval('data.questions' + str(randinfo))
        Globals.answers = eval('data.answers' + str(randinfo))
        Globals.emotion = eval('data.emotions' + str(randinfo))
        pygame.mixer.music.stop()
        if levelNum > 0:
            Globals.actualMusic = 'res/sounds/Musica/music' + \
                str(random.randint(1, 3)) + '.ogg'
            pygame.mixer.music.load(Globals.actualMusic)
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)
        self.powerups = []
        for i in range(0, 4, 1):
            Globals.ghosts[i] = ghost(i)
        if levelNum > 0:
            Globals.img_Background = pygame.image.load(
                "res/backgrounds/" + str(levelNum) + ".png")
        lineNum = -1
        rowNum = 0
        useLine = False
        isReadingLevelData = False
        for line in f:
            lineNum += 1
            while len(line) > 0 and (line[-1] == "\n" or line[-1] == "\r"):
                line = line[:-1]
            while len(line) > 0 and (line[0] == "\n" or line[0] == "\r"):
                line = line[1:]
            str_splitBySpace = line.split(' ')
            j = str_splitBySpace[0]
            if (j == "'" or j == ""):
                useLine = False
            elif j == "#":
                useLine = False
                firstWord = str_splitBySpace[1]
                if firstWord == "lvlwidth":
                    self.lvlWidth = int(str_splitBySpace[2])
                    self.levelSize = self.lvlWidth * 25
                    self.levelOffset = self.levelSize - \
                        Globals.thisGame.screenSize[0]
                elif firstWord == "lvlheight":
                    self.lvlHeight = int(str_splitBySpace[2])
                    self.levelHeight = self.lvlHeight * 25
                    self.heightOffset = self.levelHeight - \
                        Globals.thisGame.screenSize[1]
                elif firstWord == "fruittype":
                    self.fruitType = int(str_splitBySpace[2])
                    self.thisFruit = pygame.image.load(
                        "res/sprite/" + Globals.itemTypes[self.fruitType] + ".png")
                elif firstWord == "startleveldata":
                    isReadingLevelData = True
                    rowNum = 0
                elif firstWord == "endleveldata":
                    isReadingLevelData = False
            else:
                useLine = True
            if useLine:
                if isReadingLevelData:
                    for k in range(0, self.lvlWidth, 1):
                        self.SetMapTile((rowNum, k), int(str_splitBySpace[k]))
                        thisID = int(str_splitBySpace[k])
                        _x = k * 25
                        _y = rowNum * 25
                        if thisID == 4:
                            Globals.player.homeX = _x
                            Globals.player.homeY = _y
                            self.SetMapTile((rowNum, k), 0)
                        elif thisID >= 5 and thisID <= 8:
                            # one of the ghosts
                            Globals.ghosts[thisID - 5].homeX = _x
                            Globals.ghosts[thisID - 5].homeY = _y
                            self.SetMapTile((rowNum, k), 0)
                        elif thisID == 2:
                            # pellet
                            temp1 = _x + 25
                            temp2 = _y + 21
                            self.items.append([_x, temp1, _y, temp2])
                            self.pellets += 1
                        elif thisID == 3:
                            temp1 = _x + 50
                            temp2 = _y + 41
                            self.powerups.append([_x, temp1, _y, temp2, 1])
                    rowNum += 1
        Globals.GetCrossRef()
        self.Restart()

    def Restart(self):
        for k, item in Globals.ghosts.items():
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
