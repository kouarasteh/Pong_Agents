from pongPlayer import PongPlayer
from collections import namedtuple

pongState = namedtuple('pongState','ball_x ball_y vel_x vel_y paddle_y')

class PongEnvironment():

    def __init__(self,numplayers):
        self.slowingFactor = 0.5
        self.WINDOWWIDTH = 1
        self.WINDOWHEIGHT = 1
        self.paddleLength = 0.2
        self.ballCenterX = 0.5
        self.ballCenterY = 0.5
        self.rightpaddleTopY = (0.5 - (self.paddleLength/2))
        self.rightpaddleTopYIN = (0.5 - (self.paddleLength/2))
        self.ballVX = 0.03 * self.slowingFactor
        self.ballVY = 0.01 * self.slowingFactor
        self.ballVXin = 0.03 * self.slowingFactor
        self.ballVYin = 0.01 * self.slowingFactor
        self.numGamesPlayed = 0
        self.numBallsRebounded = 0
        self.hitsthisGame = 0
        self.totalHitsforAllGames = []
        self.numPlayers = numplayers
        if self.numPlayers == 2:
            self.leftpaddleTopY = (0.5 - (self.paddleLength/2))
            self.leftpaddleTopYIN = (0.5 - (self.paddleLength/2))
        self.aiscore = 0
        self.humanscore = 0
    def updateBallPosition(self):
        #update the next velocities based on edge cases right wall, top wall, bottom wall, left wall

        # if hit the right wall
        if self.ballCenterX+self.ballVX >= self.WINDOWWIDTH:
            #if hit the paddle
            if (round(self.ballCenterY,3) >= self.rightpaddleTopY) and (round(self.ballCenterY,3) <= (self.rightpaddleTopY + self.paddleLength)):
                self.hitsthisGame += 1
                self.ballVXin = -self.ballVX
                self.ballVYin = self.ballVY
                self.numBallsRebounded += 1
            #if ball goes past paddle, maintain velocity
            else:
                self.ballCenterX = self.WINDOWWIDTH
                self.ballVXin = 0
                self.ballVYin = self.ballVY
                self.humanscore += 1
                return

        #if hit the top wall
        if self.ballCenterY + self.ballVY <= 0:
            self.ballVXin = self.ballVX
            self.ballVYin = -self.ballVY

        #if hit the bottom wall
        if self.ballCenterY + self.ballVY >= self.WINDOWHEIGHT:
            self.ballVXin = self.ballVX
            self.ballVYin = -self.ballVY

        #if hit the left wall

        #if we are playing 2 player game, check for left paddle
        if self.ballCenterX+self.ballVX <= 0:
            if self.numPlayers == 2:
                #if hit the paddle
                if (round(self.ballCenterY,3) >= self.leftpaddleTopY) and (round(self.ballCenterY,3) <= (self.leftpaddleTopY + self.paddleLength)):
                    self.ballVXin = -self.ballVX
                    self.ballVYin = self.ballVY
                #if ball goes past paddle, maintain velocity
                else:
                    self.aiscore += 1
                    self.ballCenterX = 0
                    self.ballVXin = 0
                    self.ballVYin = self.ballVY
                    return
            else:
                self.ballVYin = self.ballVY
                self.ballVXin = -self.ballVX


        #now update positions based on new velocities
        self.ballCenterX += self.ballVXin
        self.ballCenterY += self.ballVYin
        self.ballVX = self.ballVXin
        self.ballVY = self.ballVYin




    def updatePaddlePosition(self):
        #if instruction goes past the top wall
        if self.rightpaddleTopYIN < 0:
            self.rightpaddleTopYIN = 0
        #if instruction goes past the bottom wall
        if (self.rightpaddleTopYIN + self.paddleLength) > self.WINDOWHEIGHT:
            self.rightpaddleTopYIN = (self.WINDOWHEIGHT - self.paddleLength)

        #update paddle location
        self.rightpaddleTopY = self.rightpaddleTopYIN

    def updateHumanPaddle(self,humanin):
        #if instruction goes past the top wall
        if self.leftpaddleTopYIN < 0:
            self.leftpaddleTopYIN = 0

        #if instruction goes past the bottom wall
        if (self.leftpaddleTopYIN + self.paddleLength) > self.WINDOWHEIGHT:
            self.leftpaddleTopYIN = (self.WINDOWHEIGHT - self.paddleLength)

        #update paddle location
        if humanin == 'up':
            self.leftpaddleTopYIN += -0.025
        elif humanin == 'down':
            self.leftpaddleTopYIN += 0.025
        elif humanin == 'none':
            self.leftpaddleTopYIN += 0
        self.leftpaddleTopY = self.leftpaddleTopYIN

    def isgameEnded(self):
        if self.ballCenterX == self.WINDOWWIDTH or (self.ballCenterX == 0 and self.numPlayers == 2):
            return True
        return False

    def resetGame(self):
        self.ballCenterX = 0.5
        self.ballCenterY = 0.5
        self.rightpaddleTopY = (0.5 - (self.paddleLength/2))
        self.rightpaddleTopYIN = (0.5 - (self.paddleLength/2))
        self.ballVX = 0.03
        self.ballVY = 0.01
        self.ballVXin = 0.03
        self.ballVYin = 0.01
        self.numGamesPlayed += 1
        self.numBallsRebounded = 0
        #print(self.hitsthisGame)
        x = self.hitsthisGame
        self.totalHitsforAllGames.append(x)
        self.hitsthisGame = 0
        #print("got to reset game")

    def resetCounters(self):
        print(self.totalHitsforAllGames)
        self.aiscore = 0
        self.humanscore = 0
        self.totalHitsforAllGames = []

    def movePaddle(self, dir):
        if dir == 'up':
            self.rightpaddleTopYIN = self.rightpaddleTopY-0.04
        elif dir == 'down':
            self.rightpaddleTopYIN = self.rightpaddleTopY+0.04
        elif dir == 'none':
            self.rightpaddleTopYIN = self.rightpaddleTopY
        # elif playerNum == 1:
        #     if dir == 'up':
        #         self.leftpaddleTopYIN = self.leftpaddleTopY-0.04
        #     elif dir == 'down':
        #         self.leftpaddleTopYIN = self.leftpaddleTopY+0.04
        #     elif dir == 'none':
        #         self.leftpaddleTopYIN = self.leftpaddleTopY

    def printGameState(self):
        print("ball Center : (",self.ballCenterX,",",self.ballCenterY,")")
        print("ball Velocity : (",self.ballVX,",",self.ballVY,")")
        print("paddle location : (",self.rightpaddleTopY,",",self.rightpaddleTopY + self.paddleLength,")")
        print(self.numBallsRebounded," balls rebounded so far")

    def iterate(self, pongPlayer):
        if self.isgameEnded():
            # print("Game ended, with ball y position: ",self.ballCenterY,
            # " and ball x position: ",self.ballCenterX,
            # " with paddle top location: ",self.rightpaddleTopY," to ",self.rightpaddleTopY + self.paddleLength)
            #print("game ended")
            self.resetGame()
        decision = pongPlayer.getNextAction(
                            pongPlayer.discretizeLocs(pongState(self.ballCenterX,
                                                                self.ballCenterY,
                                                                self.ballVX,
                                                                self.ballVY,
                                                                self.rightpaddleTopY)))
        # if self.numPlayers == 2:
        #     self.movePaddle(decision,2)
        #     self.movePaddle(humanInput,1)
        self.movePaddle(decision)
        self.updatePaddlePosition()
        self.updateBallPosition()

# pongBoard = PongEnvironment()
# pplayer = PongPlayer()
# pongBoard.resetGame()

    #print info about the positions
#    pongBoard.printGameState()
    # print("state discretized as: ",pongPlayer.discretizeLocs(pongState(pongBoard.ballCenterX,
    #                                                          pongBoard.ballCenterY,
    #                                                          pongBoard.ballVX,
    #                                                          pongBoard.ballVY,
    #                                                          pongBoard.rightpaddleTopY)))
    #update the ball and paddle
