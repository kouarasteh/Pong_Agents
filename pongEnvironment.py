from pongPlayer import PongPlayer
from collections import namedtuple

pongState = namedtuple('pongState','ball_x ball_y vel_x vel_y paddle_y')

class PongEnvironment():

    def __init__(self):
        self.WINDOWWIDTH = 1
        self.WINDOWHEIGHT = 1
        self.paddleLength = 0.2
        self.ballCenterX = 0.5
        self.ballCenterY = 0.5
        self.paddleTopY = (0.5 - (self.paddleLength/2))
        self.paddleTopYIN = (0.5 - (self.paddleLength/2))
        self.ballVX = 0.03
        self.ballVY = 0.01
        self.ballVXin = 0.03
        self.ballVYin = 0.01
        self.numGamesPlayed = 0
        self.numBallsRebounded = 0
    def updateBallPosition(self):
        #update the next velocities based on edge cases right wall, top wall, bottom wall, left wall
        print(self.ballCenterX)
        # if hit the right wall
        if self.ballCenterX == self.WINDOWWIDTH:
            #if hit the paddle
            print("ball Center : (",self.ballCenterX,",",self.ballCenterY,")")
            print("paddle location : (",self.paddleTopY,",",self.paddleTopY + self.paddleLength,")")
            if (self.ballCenterY >= self.paddleTopY) and (self.ballCenterY <= (self.paddleTopY + self.paddleLength)):
                print("HITHITHITHITHITHITHITHITHITHITHITHITHITHITHITHITHITHITHITHITHITHITHITHIT")
                self.ballVXin = -self.ballVX
                self.ballVYin = self.ballVY
                self.numBallsRebounded += 1
            #if ball goes past paddle, maintain velocity
            else:
                self.ballVXin = 0
                self.ballVYin = self.ballVY

        #if hit the top wall
        elif self.ballCenterY == 0:
            self.ballVXin = self.ballVX
            self.ballVYin = -self.ballVY

        #if hit the bottom wall
        elif self.ballCenterY == self.WINDOWHEIGHT:
            self.ballVXin = self.ballVX
            self.ballVYin = -self.ballVY

        #if hit the left wall
        elif self.ballCenterX == 0:
            self.ballVXin = - self.ballVX
            self.ballVYin = self.ballVY

        #now update positions based on new velocities
        self.ballCenterX += self.ballVXin
        self.ballCenterY += self.ballVYin
        self.ballVX = self.ballVXin
        self.ballVY = self.ballVYin




    def updatePaddlePosition(self):
        #if instruction goes past the top wall
        if self.paddleTopYIN < 0:
            self.paddleTopYIN = 0
        #if instruction goes past the bottom wall
        if (self.paddleTopYIN + self.paddleLength) > self.WINDOWHEIGHT:
            self.paddleTopYIN = (self.WINDOWHEIGHT - self.paddleLength)

        #update paddle location
        self.paddleTopY = self.paddleTopYIN


    def isgameEnded(self):
        if self.ballCenterX > self.WINDOWWIDTH and not ((self.ballCenterY >= self.paddleTopY)
                                                        and (self.ballCenterY <= (self.paddleTopY + self.paddleLength))):
            return True
        return False

    def resetGame(self):
        self.ballCenterX = 0.5
        self.ballCenterY = 0.5
        self.paddleTopY = (0.5 - (self.paddleLength/2))
        self.paddleTopYIN = (0.5 - (self.paddleLength/2))
        self.ballVX = 0.03
        self.ballVY = 0.01
        self.ballVXin = 0.03
        self.ballVYin = 0.01
        self.numGamesPlayed += 1

    def movePaddle(self, dir):
        if dir == 'up':
            self.paddleTopYIN = self.paddleTopY-0.04
        elif dir == 'down':
            self.paddleTopYIN = self.paddleTopY+0.04
        elif dir == 'none':
            self.paddleTopYIN = self.paddleTopY

    def printGameState(self):
        print("ball Center : (",self.ballCenterX,",",self.ballCenterY,")")
        print("ball Velocity : (",self.ballVX,",",self.ballVY,")")
        print("paddle location : (",self.paddleTopY,",",self.paddleTopY + self.paddleLength,")")
        print(self.numBallsRebounded," balls rebounded so far")

    def iterate(self, pongPlayer):
        decision = pongPlayer.getNextAction(
                            pongPlayer.discretizeLocs(pongState(self.ballCenterX,
                                                                self.ballCenterY,
                                                                self.ballVX,
                                                                self.ballVY,
                                                                self.paddleTopY)))
        self.movePaddle(decision)
        self.updatePaddlePosition()
        self.updateBallPosition()
        # if self.isgameEnded():
        #     print("Game ended, with ball y position: ",self.ballCenterY,
        #     " and ball x position: ",self.ballCenterX,
        #     " with paddle top location: ",self.paddleTopY," to ",self.paddleTopY + self.paddleLength)
        #     self.resetGame()
# pongBoard = PongEnvironment()
# pplayer = pongPlayer()
# pongBoard.resetGame()

    #print info about the positions
#    pongBoard.printGameState()
    # print("state discretized as: ",pongPlayer.discretizeLocs(pongState(pongBoard.ballCenterX,
    #                                                          pongBoard.ballCenterY,
    #                                                          pongBoard.ballVX,
    #                                                          pongBoard.ballVY,
    #                                                          pongBoard.paddleTopY)))
    #update the ball and paddle
