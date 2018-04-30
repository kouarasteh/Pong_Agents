import pygame, sys, math
from pygame.locals import *
from pongEnvironment import PongEnvironment
from pongPlayer import PongPlayer
BLACK     = (0  ,0  ,0  )
RED     = (255,0,0)
WHITE     = (255,255,255)

class pongVisualizer():

    def __init__(self,width,height,ballr,linethicc,paddlesize):
        self.winwidth = width
        self.winheight = height
        self.ballrad = ballr
        self.thicc = linethicc
        self.pad = paddlesize

    def drawBoard(self,bx,by,pady):
        pygame.draw.rect(gameDisplay,
                         BLACK,
                         [self.winwidth-self.thicc,
                          pady,
                          self.thicc,
                          self.pad])
        pygame.draw.circle(gameDisplay,
                           RED,
                           (math.floor(bx),math.floor(by)),self.ballrad,0)



pv = pongVisualizer(600,600,10,10,120)
board = PongEnvironment()
pplayer = PongPlayer()
#board.resetGame()

pygame.init()
gameDisplay = pygame.display.set_mode((pv.winwidth,pv.winheight))
pygame.display.set_caption('PONG')
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 25)


crashed = False
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
            print(event)
    board.iterate(pplayer)
    text = font.render("Games Played: "+str(board.numGamesPlayed), True, BLACK)
    text2 = font.render("Balls Rebounded: "+str(board.numBallsRebounded), True, BLACK)
    gameDisplay.fill(WHITE)
    gameDisplay.blit(text,(0,0))
    gameDisplay.blit(text2,(0,30))
    pv.drawBoard(pv.winwidth  * board.ballCenterX,
                 pv.winheight * board.ballCenterY,
                 pv.winheight * board.paddleTopY)
    pygame.display.update()
    clock.tick(60)
