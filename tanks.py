#------------------------------------------
# CHALLENGING PARTS
# 1. level screen
# 2. buttons function
# 3. Bullet graphics
#-------------------------------------------
# MY CONTRIBUTION
# Changed the game working structure
# Added extra enemy movements and better AI
# Added Game levels
# Over tank hovering power meter
# Multiple random barriers
# Better bullet graphics
# Better game sounds
# Points (still to be added)
#-------------------------------------------

import pygame
from pygame.locals import *
import sys
import time
import random
pygame.init()
pygame.display.set_caption('TanksGame')

# Colors
white = (255,255,255)
black = (0,0,0)
grey = (221,215,215)
lightgrey = (245,243,243)
red = (220,0,0)         
lightRed = (255,0,0)
yellow = (220,220,0)
lightYellow = (255,255,0)
green = (60, 197, 60)
lightGreen = (0,255,0)
blue = (0,0,220)
lightBlue = (0,0,255)

# Game dimension
displayWidth = 800
displayHeight = 600
gameDisplay = pygame.display.set_mode((displayWidth,displayHeight))
FPS = 10
clock = pygame.time.Clock()

explosionSound = pygame.mixer.Sound('audio/small-explosion.aiff')
youWin = pygame.mixer.Sound('audio/youWin.wav')
youLose = pygame.mixer.Sound('audio/youLose.wav')               
            
                                    ## REMEMBER TO GIVE CREDITS
background = pygame.image.load('tankImage.jpg')
 
backgroundRect = background.get_rect()
backgroundRect.center = (displayHeight//2+100,displayWidth//2-100)


# Font setting
verySmallFont = pygame.font.SysFont('comisansms',15)
smallFont = pygame.font.SysFont('comicsansms',20)
mediumFont = pygame.font.SysFont('impact',45)
largeFont = pygame.font.SysFont('impact',70)
veryLargeFont = pygame.font.SysFont('impact',100)

#  FINALLY                                             //
#  IT IS COMPLETED                                    //
#  TOOK MUCH LONGER THAN EXPECTED                \\  //
#  ALSO, DIDN'T USE OBJECT ORIENTED APPROACH      \\//
#  BUT ATLEAST I MADE IT!!!                        \/

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    PUT TO GITHUB    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



##################################################### TEXT AND BUTTONS #############################################################


def textObject(text,color,size):
    """ making the text object with text,color,size """
    
    if size == 'verySmall':
        textSurface = verySmallFont.render(text,True,color)
    if size == 'small':
        textSurface = smallFont.render(text,True,color)
    elif size == 'medium':
        textSurface = mediumFont.render(text,True,color)
    elif size == 'large':
        textSurface = largeFont.render(text,True,color)
    elif size == 'veryLarge':
        textSurface = veryLargeFont.render(text,True,color)
    return textSurface,textSurface.get_rect()


# Still not used the features of class instead of a function
class messageToScreen(pygame.sprite.Sprite):
    def __init__(self,text, color, x_disp=0, y_disp=0, size='small',background=None):
        self.text = text
        self.color = color
        self.size = size
        self.background = background
        textSurface,textRect = textObject(text,color,size)
        textRect.center = (displayWidth/2 + x_disp), (displayHeight/2 + y_disp)
        if(background):
            gameDisplay.fill(Color(background),textRect)
        gameDisplay.blit(textSurface,textRect)



def textOfButton(text, color, buttonX,buttonY,buttonWidth,buttonHeight, size='small'):
    ''' To put text on a button '''

    textSurface,textRect = textObject(text, color, size)
    textRect.center = ((buttonX)+(buttonWidth/2)),((buttonY)+(buttonHeight/2))
    gameDisplay.blit(textSurface,textRect)



def button(text,x,y,width,height,inactiveColor,activeColor,action=None):
    ''' To create a button '''

    cur = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()

    if x+width > cur[0] > x and y+height > cur[1] > y:
        if clicked[0] == 1 and action != None:
            if action == 'play':
                gameLevel = levelScreen()
                return gameLevel
            elif action == 'control':
                controlScreen()
            elif action == 'quit':
                pygame.quit()
                sys.exit(0)
            elif action == 'tutorial':
                tutorialScreen()
            elif action == 'continue':
                return False
            elif action == 'escape':
                return False
            # elif action == 'level1':
            #     return 1
            # elif action == 'level2':
            #     return 2
            elif action == 'level3':
                return 3
            elif action == 'level4':
                return 4
            elif action == 'level5':
                return 5
        pygame.draw.rect(gameDisplay, activeColor, (x,y,width,height))
    else:
        pygame.draw.rect(gameDisplay, inactiveColor, (x,y,width,height))
    textOfButton(text,black,x,y,width,height)

#--------------------------------------------------------------------- END OF TEXT AND BUTTONS ---------------------------------------------------------------











########################################################### GAME OBJECTS #######################################################################

turretX = 30
turretY = 10
turretWidth = 3
wheelWidth = 5
groundHeight = displayHeight * 0.9


def tank(x,y,tankHeight,tankWidth,turpos):
    x=int(x)
    y=int(y)

    turretPositions = [ 
                        (x-27,y-2),
                        (x-26,y-5),
                        (x-25,y-8),
                        (x-23,y-12),
                        (x-21,y-14),
                        (x-18,y-15),
                        (x-15,y-17),
                        (x-13,y-19),
                        (x-11,y-21) 
                      ]
    
    # Tank head,body,and turret
    pygame.draw.circle(gameDisplay, black, (x,y), tankHeight//2)
    pygame.draw.rect(gameDisplay, black, (x-tankWidth//2,y,tankWidth,tankHeight))
    pygame.draw.line(gameDisplay,black,(x,y),turretPositions[turpos],turretWidth)
    
    # Tank wheels
    startX = x-tankWidth//2+2
    for _ in range(tankWidth//wheelWidth):
        pygame.draw.circle(gameDisplay,black,(startX,y+tankHeight),wheelWidth)
        startX = startX + wheelWidth
    return turretPositions[turpos]



def enemyTank(x,y,tankHeight,tankWidth):
    ''' Makes the enemy tank '''

    x=int(x)
    y=int(y)

    turretPositions = [
                       (x+27,y-2),
                       (x+26,y-5),
                       (x+25,y-8),
                       (x+23,y-12),
                       (x+21,y-14),
                       (x+18,y-15),
                       (x+15,y-17),
                       (x+13,y-19),
                       (x+11,y-21)
                      ]
    
    # tank head,body,and turret
    pygame.draw.circle(gameDisplay, black, (x,y), tankHeight//2)
    pygame.draw.rect(gameDisplay, black, (x-tankHeight,y,tankWidth,tankHeight))

    # To CHANGE the turpos (if needed)
    pygame.draw.line(gameDisplay,black,(x,y),turretPositions[8],turretWidth)
    
    # Tank wheels
    startX = x-tankWidth//2+2
    for _ in range(tankWidth//wheelWidth):
        pygame.draw.circle(gameDisplay,black,(startX,y+tankHeight),wheelWidth)
        startX = startX + wheelWidth
    return turretPositions[8]



def explosion(hitX,hitY,expSize=50):
    ''' It makes the explosion graphics ''' 

    pygame.mixer.Sound.play(explosionSound)
    magnitude = 1
    colors = [red,lightRed,yellow,lightYellow]
    while magnitude < expSize:
        pygame.display.update()
        expLocX = hitX + random.randrange(-1*magnitude, magnitude)
        expLocY = hitY + random.randrange(-1*magnitude,magnitude)
        bitsSize = random.randrange(1,5)
        if expLocY >= groundHeight:
            pygame.draw.circle(gameDisplay,green,(expLocX,expLocY), bitsSize)
        else:
            pygame.draw.circle(gameDisplay,colors[random.randrange(0,3)],(expLocX,expLocY), bitsSize)
        magnitude+=1




def findingTarget(loc,tankX,tankY,tankWidth,barrierList,gameLevel=3):
    ''' Finds the target for enemy '''
    turPos = 8
    targetFound = False
    currentPower = 10
    while not targetFound:
        fire = True
        startShellPos = list(loc) 
        currentPower += 1

        if currentPower > 100:
            currentPower = random.randint(50,80)
            break

        while fire:

            # if bullet hit ground and/or tank
            if startShellPos[1] >= groundHeight-10:       # subtracted 10 for more realistic collision 
                if(tankX-(tankWidth//2) < startShellPos[0] < tankX+(tankWidth//2)):
                    targetFound = True
                fire = False
                
                hitX = int((startShellPos[0]*displayHeight)/startShellPos[1])
                hitY = startShellPos[1]
            

            # If bullet hit barriers
            for barrier in barrierList:
                barrierX = barrier[0]
                barrierHeight = barrier[1]
                barrierWidth = barrier[2]
                checkX = (barrierX + barrierWidth) >= startShellPos[0] >= barrierX
                checkY = groundHeight >= startShellPos[1] >= groundHeight-barrierHeight
                if checkX and checkY:
                    fire = False

            startShellPos[0] += (12-turPos)*2
            startShellPos[1] += int(((startShellPos[0]-loc[0])*(0.009/(currentPower/90)))**2 - (turPos+turPos/(12-turPos)))

            clock.tick(2000)
    
    # Randomness to the shot according to gameLevel
    gameLevel = (5.5-gameLevel)/10

    low = int(currentPower*(1.0-gameLevel))
    high = int(currentPower*(1.0+gameLevel))
    if(low!=high):
        currentPower = random.randrange(low,high)
    return (targetFound,currentPower)




def fire(displayHeight,displayWidth,loc,tankX,tankY,tankWidth,
        enemyTankX,enemyTankY,turPos,firePower,
        barrierList,user='player',gameLevel=3):
    fire = True
    startShellPos = list(loc)
    damage = 0

    while fire:

        # If bullet hit ground or target
        # subtracted 10 for more realistic ground collision
        if startShellPos[1] >= groundHeight-10:      
            if enemyTankX+15 > startShellPos[0] > enemyTankX-15: 
                damage = 20
            elif enemyTankX+40 > startShellPos[0] > enemyTankX-40: 
                damage = 10
            elif enemyTankX+50 > startShellPos[0] > enemyTankX-50: 
                damage = 5
            explosion(startShellPos[0], startShellPos[1])
            fire = False
        
        
        # If bullet hit barriers
        for barrier in barrierList:
            barrierX = barrier[0]
            barrierHeight = barrier[1]
            barrierWidth = barrier[2]
            checkX = (barrierX + barrierWidth) >= startShellPos[0] >= barrierX
            checkY = groundHeight >= startShellPos[1] >= groundHeight-barrierHeight
            if checkX and checkY:
                fire = False
                explosion(startShellPos[0],startShellPos[1])


        # Drawing the bullet
        oldbullet = pygame.draw.circle(gameDisplay,white,(startShellPos[0], startShellPos[1]),3)

        # Bullet physics i.e.(changing startShellPos[0] and startShellPos[1])
        if user=="player":
            startShellPos[0] -= (12-turPos)*2
        elif user=="enemy":
            startShellPos[0] += (12-turPos)*2
        startShellPos[1] += int(((startShellPos[0]-loc[0])*(0.009/(firePower/90)))**2 - (turPos+turPos/(12-turPos)))

        ## drawing the bullet
        newbullet = pygame.draw.circle(gameDisplay,red,(startShellPos[0], startShellPos[1]),3)

        pygame.display.update([oldbullet,newbullet])
        clock.tick(40)
    return damage


def barrier(barrierList):
    ''' Makes the barriers '''

    for barrier in barrierList:
        pygame.draw.rect(gameDisplay, black, (barrier[0], groundHeight-barrier[1], barrier[2], barrier[1]))



def ground(height):
    gameDisplay.fill(green,rect=[0, height, displayWidth,displayHeight - height])



def healthBar(playerHealth,enemyHealth):
    ''' Diplay the health bars on screen'''

    playerHealthColor = green
    enemyHealthColor = green

    if playerHealth > 75:
        playerHealthColor = green
    elif playerHealth > 50:
        playerHealthColor = yellow
    else:
        playerHealthColor = red
        
    if enemyHealth > 75:
        enemyHealthColor = green
    elif enemyHealth > 50:
        enemyHealthColor = yellow
    else:
        enemyHealthColor = red

    messageToScreen("Player",playerHealthColor,300,-290,size='small')
    pygame.draw.rect(gameDisplay,playerHealthColor,(670,25,playerHealth,25))
    messageToScreen("CPU",enemyHealthColor,-360,-290,size='small')
    pygame.draw.rect(gameDisplay,enemyHealthColor,(20,25,enemyHealth,25))


def FirepowerMeter(power,tankX,tankY):
    ''' Shows the fire power meter on screen '''

    textSurf, textRect = textObject(f'Power: {power}%', red, size="small")
    textRect.center = (tankX,tankY-30)
    if textRect.x + textRect.width > displayWidth:
        textRect.center = (displayWidth-textRect.width//2,tankY-30)

    gameDisplay.blit(textSurf,textRect)
#----------------------------------------------------------------  GAME OBJECTS ------------------------------------------------------------------













############################################################### GAME MENUS ############################################################


def paused(gameOn):
    ''' paused screen logic '''
    gameOn = True
    paused = True


    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    paused = False
        
        gameDisplay.blit(background,backgroundRect)
         

        messageToScreen('Game Paused', red, y_disp=-50, size="large")       
        contReturned = button('Continue',200, 320, 100, 50, green, lightGreen, action='continue')
        button('Controls',350, 320, 100, 50, yellow, lightYellow, action='control')
        escReturned = button('Escape', 500, 320, 100, 50, red, lightRed, action='escape')

        if contReturned == False:
            paused = contReturned
        elif escReturned == False:
            paused = escReturned
            gameOn = escReturned
        pygame.display.update()
        clock.tick(FPS)
    return gameOn


def controlScreen():
    ''' shows the controls of the game'''
    showControl = True

    # gameDisplay.fill(white)
    gameDisplay.blit(background,backgroundRect)
     


    messageToScreen('Controls', red, y_disp=-50, size = 'large')
    messageToScreen('Fire: Space',black, y_disp=20,size='small', background="white")
    messageToScreen('Move Turret: Up and Down arrows', black, y_disp=50,size='small', background="white")
    messageToScreen('Move Tank: Left and Right arrows', black, y_disp=80,size='small', background="white")
    messageToScreen('Power Up: Z',black, y_disp=110,size='small', background="white")
    messageToScreen('Power Down: X',black, y_disp=140,size='small', background="white")
    messageToScreen('Pause: Esc',black, y_disp=170,size='small', background="white")

    while showControl:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
       
        returned = button('Back',350,500,100,50,green,lightGreen,action='continue')
        if returned == False:
            showControl = False

        pygame.display.update()

def tutorialScreen():
    ''' Displays the tutorial to play the game '''

    gameDisplay.blit(background,backgroundRect)
     


    messageToScreen('How To Play', red, y_disp=-50, size = 'large')
    messageToScreen('You are the right tank',black, y_disp=20,size='small', background="white")
    messageToScreen('You have to fire at the enemy', black, y_disp=50,size='small', background="white")
    messageToScreen('The enemy will fire back', black, y_disp=80,size='small', background="white")
    messageToScreen('You can move left or right before firing',black, y_disp=110,size='small', background="white")
    messageToScreen('You can also change the turret position',black, y_disp=140,size='small', background="white")
    messageToScreen('You can adjust the fire power',black, y_disp=170,size='small', background="white")
    messageToScreen('The first to get knocked out loses!!',black, y_disp=200,size='small', background="white")

    showTut = True
    while(showTut):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        returned = button('Back',350,530,100,50,green,lightGreen,action='continue')
        if returned == False:
            showTut = False
        pygame.display.update()
        

        
def WonScreen(showIntro):
    ''' The Won screen '''
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.Sound.play(youWin)
    paused = True
    messageToScreen('You Win !!!', red, y_disp=-50, size='large')

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    paused = False
        
        contRet = button('Play Again',270, 320, 100, 50, green, lightGreen, action='continue')
        escRet = button('I\'m Done', 430, 320, 100, 50, yellow, lightYellow, action='escape')

        if contRet == False:
            paused = contRet
            showIntro = False
        elif escRet == False:
            paused = escRet
            gameOn = escRet
            showIntro = True

        pygame.display.update()
        clock.tick(FPS)
    pygame.mixer.music.set_volume(0.7)
    return showIntro


def LostScreen(showIntro):
    ''' The Lost screen '''
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.Sound.play(youLose)
    paused = True
    messageToScreen('You Lose', red, y_disp=-50, size='large')
    messageToScreen('Better luck next time', green, y_disp=10, size='medium')

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    paused = False
        
        contReturned = button('Play Again',250, 350, 100, 50, green, lightGreen, action='continue')
        escReturned = button('I\'m Done', 450, 350, 100, 50, yellow, lightYellow, action='escape')

        if contReturned == False:
            paused = contReturned
            showIntro = False
        elif escReturned == False:
            paused = escReturned
            showIntro = True

        pygame.display.update()
        clock.tick(FPS)
    pygame.mixer.music.set_volume(0.7)
    return showIntro

def levelScreen():
    started = True
    while(started):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    started = False
        # gameDisplay.fill(white)
        gameDisplay.blit(background,backgroundRect)
         


        messageToScreen("Choose Difficulty Level",red,0,-50,size='large')
        level3 = button('Easy',200,330,120,45,yellow,lightYellow,action='level3')
        level4 = button('Medium',350,330,120,45,green,lightGreen,action='level4')
        level5 = button('Hard',500,330,120,45,red,lightRed,action='level5')
        # if(level1 != None):
        #     return level1
        # if(level2 != None):
        #     return level2
        if(level3 != None):
            return level3
        if(level4 != None):
            return level4
        if(level5 != None):
            return level5
        pygame.display.update()



def introScreen():
    ''' shows the intro screen of the game'''

    intro = True
    pygame.mixer.music.load('audio/99699__knarmahfox__over-world-intro.wav')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.7)

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameLoop()
                if  event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)

        gameDisplay.blit(background,backgroundRect)
         

        messageToScreen('TANKS GAME', red, y_disp=-20, size = 'veryLarge')

        playReturned = button('Play',200,370,100,50,green,lightGreen,action='play')
        button('How To Play',350,370,120,50,yellow,lightYellow,action='tutorial')
        button('Exit',510,370,100,50,red,lightRed,action='quit')
        if(playReturned):
            return playReturned
        pygame.display.update()
                



def gameLoop(showIntro, gameLevel=3):
    '''the main loop of the game'''
    gameOn = True

    # GAME MUSIC
    pygame.mixer.music.load('audio/inGameMusic.wav')
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1)


    # TANK POSITION
    tankMove = 0
    tankWidth = 40
    tankHeight = 20
    mainTankX = displayWidth * 0.9
    mainTankY = groundHeight - tankHeight - wheelWidth
    enemyTankX = displayWidth * 0.1
    enemyTankY = displayHeight * 0.9 - tankHeight - wheelWidth
    
    # TURRET POSITION AND POWER
    turPos = 0
    curTurPos = 0
    firePower = 50
    powerChange = 0
    
    # HEALTH
    playerHealth = 100
    enemyHealth = 100

    # BARRIERS 
    barrierList = []

    barrierX = displayWidth/2 + random.randint(int((displayWidth/2)*-0.55),int((displayWidth/2)*-0.45))
    barrierWidth = 20
    noOfBarriers = random.randint(10,22)
    endingBarriers = int(noOfBarriers*0.2)
    sideBarriers = int(noOfBarriers*0.4)
    for i in range(noOfBarriers):
        if i<endingBarriers or i>noOfBarriers-endingBarriers:
            barrierHeight = random.randrange(int(displayHeight*0.17),int(displayHeight*0.30))
        elif i<sideBarriers or i>noOfBarriers-sideBarriers:
            barrierHeight = random.randrange(displayHeight*0.25,displayHeight*0.4)
        else:
            barrierHeight = random.randrange(displayHeight*0.30,displayHeight*0.45)
        barrierList.append((barrierX,barrierHeight,barrierWidth))
        barrierX += barrierWidth
    # For constructing barriers
    barrier(barrierList)

    while gameOn:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameOn = paused(showIntro)
                elif event.key == pygame.K_LEFT:
                    tankMove -= 5
                elif event.key == pygame.K_RIGHT:
                    tankMove += 5
                elif event.key == pygame.K_UP:
                    curTurPos += 1
                elif event.key == pygame.K_z:
                    powerChange += 1
                elif event.key == pygame.K_x:
                    powerChange += -1
                elif event.key == pygame.K_DOWN:
                    curTurPos -= 1
                elif event.key == pygame.K_SPACE:
                    damage = fire(displayHeight,displayWidth,gun,mainTankX,mainTankY, 
                                tankWidth,enemyTankX,enemyTankY, turPos,firePower,
                                barrierList, user='player',gameLevel=gameLevel)
                    enemyHealth -= damage
                    if enemyHealth <= 0:
                        gameOn = False
                        showIntro = WonScreen(showIntro)
                        break

                    gameDisplay.fill(white)

                    ground(groundHeight)
                    barrier(barrierList)
                    healthBar(playerHealth,enemyHealth)
                    # FirepowerMeter(firePower,mainTankX,mainTankY)
                    gun = tank(mainTankX,mainTankY,tankHeight,tankWidth,turPos)
                    enemyGun = enemyTank(enemyTankX,enemyTankY,tankHeight,tankWidth)
                    pygame.display.update()

                    # Enemy movement (Artificial Intelligence)
                    enemyFirePower = firePower
                    shotDone = False
                    # The higher the difficulty, the more chances for the enemy
                    chances = gameLevel

                    while(not shotDone and chances):
                        possibleMovements = (-2,2)
                        if(enemyTankX >= barrierList[0][0]):
                            moveDir = 0
                        elif(enemyTankX <= tankWidth):
                            moveDir = 1
                        else:
                            moveDir = random.randrange(0,1)
                        distToMove = random.randrange(5,35)
                        for i in range(distToMove):
                            enemyTankX += possibleMovements[moveDir]
                            if(enemyTankX-tankWidth//2 < 0):
                                break

                            # Refreshing the screen after enemy tank moved
                            gameDisplay.fill(white)
                            ground(groundHeight)
                            barrier(barrierList)
                            healthBar(playerHealth,enemyHealth)
                            # FirepowerMeter(firePower,mainTankX,mainTankY)
                            gun = tank(mainTankX,mainTankY,tankHeight,tankWidth,turPos)
                            enemyGun = enemyTank(enemyTankX,enemyTankY,tankHeight,tankWidth)
                            pygame.display.update()
                            clock.tick(FPS+5)
                        shotDone,enemyFirePower = findingTarget(enemyGun, mainTankX, mainTankY, tankWidth, barrierList, gameLevel=gameLevel)
                        chances -= 1

                    damage = fire(displayHeight,displayWidth,enemyGun,enemyTankX,enemyTankY,
                                tankWidth,mainTankX,mainTankY, 8,
                                enemyFirePower,barrierList,user='enemy',gameLevel=gameLevel)
                    playerHealth -= damage
                    if playerHealth <= 0:
                        gameOn = False
                        showIntro = LostScreen(showIntro)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                    tankMove = 0
                if event.key == pygame.K_UP or pygame.K_DOWN:
                    curTurPos = 0
                if event.key == pygame.K_z or pygame.K_x:
                    powerChange = 0
        
        gameDisplay.fill(white)

        
        # Ground
        ground(groundHeight)
        
        # Tank moving
        mainTankX += tankMove
        if(mainTankX+tankWidth//2 > displayWidth):
            mainTankX = displayWidth-tankWidth//2

        # Fire power change
        if(0 < firePower+powerChange <= 100):
            firePower += powerChange
        FirepowerMeter(firePower, mainTankX, mainTankY)
        
        # Turret moving
        if 0 <= turPos+curTurPos < 9:
            turPos += curTurPos

        # If tank hits barrier   
            if  (mainTankX-tankWidth/2) < barrierList[len(barrierList)-1][0]+barrierWidth:
                mainTankX += 5

        barrier(barrierList)
        healthBar(playerHealth,enemyHealth)
        gun = tank(mainTankX,mainTankY,tankHeight,tankWidth,turPos) 
        enemyGun = enemyTank(enemyTankX,enemyTankY,tankHeight,tankWidth)

        if(gameOn == False):
            pygame.mixer.music.load('audio/99699__knarmahfox__over-world-intro.wav')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.7)
        pygame.display.update()
        clock.tick(FPS)
    return showIntro
#------------------------------------------------------------- END OF MENUS ----------------------------------------------------------      

showIntro = True
while True:
    if showIntro:
        introScreen()
    gameLevel = levelScreen()
    showIntro = gameLoop(showIntro, gameLevel=gameLevel)