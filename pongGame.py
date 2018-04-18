import pygame, sys
from pygame.locals import *

class pongGame():
    def __init__(self):
        self.WINDOWWIDTH = 800
        self.WINDOWHEIGHT = 600
        self.LINETHICKNESS = 10
        self.PADDLESIZE = 100
        self.PADDLEOFFSET = 20
        self.BALLRADIUS = 15
        self.paddleY = 0
        self.paddleVY = 0
        self.ballPX = 10
        self.ballPY = 0
        self.stepSize = 5
        self.ballVX = self.stepSize
        self.ballVY = self.stepSize
        # Set up the colours
        self.BLACK     = (0  ,0  ,0  )
        self.WHITE     = (255,255,255)
        self.lost = False
        self.numGamesPlayed = 0
        self.numGamesWon = 0

    def resetGame(self):
        self.paddleY = (self.WINDOWHEIGHT / 2) - (self.PADDLESIZE/2)
        self.paddleVY = 0
        self.ballPX = 10
        self.ballPY = 0
        self.ballVX = self.stepSize
        self.ballVY = self.stepSize

    def win(self):
        self.numGamesPlayed += 1
        self.numGamesWon += 1
    def lose(self):
        self.numGamesPlayed += 1
    def updatePaddle(self):
        y = self.paddleY + self.paddleVY
        actualY = y
        if y < 0:
            actualY = 0
        elif y > (self.WINDOWHEIGHT-self.PADDLESIZE):
            actualY = self.WINDOWHEIGHT - self.PADDLESIZE
        self.paddleY = actualY
        pygame.draw.rect(gameDisplay, self.BLACK, [self.WINDOWWIDTH-self.LINETHICKNESS-self.PADDLEOFFSET,actualY,self.LINETHICKNESS,self.PADDLESIZE])


    def updateBall(self,x,y):
        if self.isContact():
            self.ballVX = -self.ballVX
        if self.ballPY < self.BALLRADIUS:
            self.ballPY = self.BALLRADIUS
            self.ballVY = -self.ballVY
        if self.ballPY > (self.WINDOWHEIGHT - self.BALLRADIUS):
            self.ballPY = (self.WINDOWHEIGHT - self.BALLRADIUS)
            self.ballVY = -self.ballVY
        if self.ballPX < self.BALLRADIUS:
            print("LEFT WALL")
            self.ballPX = self.BALLRADIUS
            self.ballVX = -self.ballVX
        if self.ballPX > (self.WINDOWWIDTH - self.BALLRADIUS):
            self.lost = True
            return
        pygame.draw.circle(gameDisplay,self.BLACK,(x + self.ballVX,y + self.ballVY),self.BALLRADIUS,0)
        self.ballPX += self.ballVX
        self.ballPY += self.ballVY

    def isContact(self):
        if self.ballPY > self.paddleY and self.ballPY < (self.paddleY + self.PADDLESIZE):
            if self.ballPX == (self.WINDOWWIDTH-self.PADDLEOFFSET - self.BALLRADIUS):
                return True
        return False
    def paddleUP(self):
        self.paddleVY = -self.stepSize
    def paddleDOWN(self):
        self.paddleVY = self.stepSize
    def stopPaddle(self):
        self.paddleVY = 0


pygame.init()
pg = pongGame()
gameDisplay = pygame.display.set_mode((pg.WINDOWWIDTH,pg.WINDOWHEIGHT))
pygame.display.set_caption('A bit racey')
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 25)

crashed = False
cbx = 0
cby = 0
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == K_UP:
                pg.paddleUP()
            if event.key == K_DOWN:
                pg.paddleDOWN()
        if event.type == pygame.KEYUP:
            if event.key in (K_UP, K_DOWN):
                pg.stopPaddle()
        print(event)
    if pg.lost:
        pg.resetGame()
        pg.lost = False
        pg.lose()
    text = font.render("Games Played: "+str(pg.numGamesPlayed), True, pg.BLACK)

    print(pg.ballPX,pg.ballPY)
    gameDisplay.fill(pg.WHITE)
    gameDisplay.blit(text,(0,0))
    pg.updatePaddle()
    pg.updateBall(pg.ballPX,pg.ballPY)
    pygame.display.update()
    clock.tick(60)
