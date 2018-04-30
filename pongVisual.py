import pygame, sys, math, pickle
import numpy as np
from pygame.locals import *
from pongEnvironment import PongEnvironment
from pongPlayer import PongPlayer
BLACK     = (0  ,0  ,0  )
RED     = (255,0,0)
WHITE     = (255,255,255)
NUMPLAYERS = 1
class pongVisualizer():

    def __init__(self,width,height,ballr,linethicc,paddlesize):
        self.winwidth = width
        self.winheight = height
        self.ballrad = ballr
        self.thicc = linethicc
        self.pad = paddlesize

    def drawBoard(self,bx,by,pad1y,pad2y=0):
        pygame.draw.rect(gameDisplay,
                         BLACK,
                         [self.winwidth-self.thicc,
                          pad1y,
                          self.thicc,
                          self.pad])
        if NUMPLAYERS == 2:
            pygame.draw.rect(gameDisplay,
                             BLACK,
                             [0,
                              pad2y,
                              self.thicc,
                              self.pad])
        pygame.draw.circle(gameDisplay,
                           RED,
                           (math.floor(bx),math.floor(by)),self.ballrad,0)



pv = pongVisualizer(1200,1200,10,10,240)
board = PongEnvironment(NUMPLAYERS)
pplayer = PongPlayer()
board.resetGame()
#initial explorative training
count = 0
while count <= 50000:
    if board.isgameEnded():
        count += 1
    board.iterate(pplayer)

print(board.totalHitsforAllGames)
pickle.dump(board.totalHitsforAllGames, open('totalhits1.txt','wb'))
print("average hits per game:" , sum(board.totalHitsforAllGames)/200)
pplayer.writeToFile('q1.txt','N1.txt')
print(pplayer.q)
print(pplayer.N)

pplayer.readFromFile('q1.txt','N1.txt')
print(pplayer.q)
print(pplayer.N)
board.resetCounters()

#non explorative training
pplayer.epsilon = 0
count = 0
print("phase 1 done")
while count <= 50000:
    if board.isgameEnded():
        count += 1
    board.iterate(pplayer)

print(board.totalHitsforAllGames)
pickle.dump(board.totalHitsforAllGames, open('totalhitsgold.txt','wb'))
print("average hits per game:" , sum(board.totalHitsforAllGames)/200)
pplayer.writeToFile('qGOLD.txt','NGOLD.txt')

board.resetCounters()
#testing round of 200 games
count = 0
pplayer.readFromFile('qGOLD.txt','NGOLD.txt')
print("phase 2 done")
while count <= 200:
     if board.isgameEnded():
         count += 1
     board.iterate(pplayer)

print(board.totalHitsforAllGames)
pickle.dump(board.totalHitsforAllGames, open('twohunnitq.txt','wb'))
print("average hits per game:" , sum(board.totalHitsforAllGames)/200)
pplayer.writeToFile('q3.txt','N3.txt')

pygame.init()
gameDisplay = pygame.display.set_mode((pv.winwidth,pv.winheight))
pygame.display.set_caption('PONG')
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 25)


crashed = False
while not crashed:
    if NUMPLAYERS == 2:
        keys = pygame.key.get_pressed()  #checking pressed keys
        if keys[pygame.K_UP]:
            board.updateHumanPaddle('up')
        elif keys[pygame.K_DOWN]:
            board.updateHumanPaddle('down')
        else:
            board.updateHumanPaddle('none')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
            print(event)
        # if NUMPLAYERS == 2:
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == K_UP:
        #             board.updateHumanPaddle('up')
        #         elif event.key == K_DOWN:
        #             board.updateHumanPaddle('down')
        #         elif event.type == pygame.KEYUP:
        #             if event.key in (K_UP, K_DOWN):
        #                 board.updateHumanPaddle('none')

    board.iterate(pplayer)
    if NUMPLAYERS == 1:
        text = font.render("Games Played: "+str(board.numGamesPlayed), True, BLACK)
        text2 = font.render("Balls Rebounded: "+str(board.numBallsRebounded), True, BLACK)
    if NUMPLAYERS == 2:
        text = font.render("Games Played: "+str(board.numGamesPlayed), True, BLACK)
        text2 = font.render("Score, human/AI : "+str(board.humanscore)+"/"+str(board.aiscore), True, BLACK)
    gameDisplay.fill(WHITE)
    gameDisplay.blit(text,(0,0))
    gameDisplay.blit(text2,(0,30))
    if NUMPLAYERS == 2:
        pv.drawBoard(pv.winwidth  * board.ballCenterX,
                     pv.winheight * board.ballCenterY,
                     pv.winheight * board.rightpaddleTopY,
                     pv.winheight * board.leftpaddleTopY)
    elif NUMPLAYERS == 1:
        pv.drawBoard(pv.winwidth  * board.ballCenterX,
                     pv.winheight * board.ballCenterY,
                     pv.winheight * board.rightpaddleTopY)
    pygame.display.update()
    if NUMPLAYERS == 1:
        clock.tick(60)
    elif NUMPLAYERS == 2:
        clock.tick(60)
