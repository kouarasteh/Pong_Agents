from collections import namedtuple
import numpy as np
import math,random
paddle_height = 0.2
GAMMA = 0.77
BIGN = 20 #was 20
BIGC = 4000 #was 2
posActs = ['up','down','none']
pongState = namedtuple('pongState','ball_x ball_y vel_x vel_y paddle_y')
        # #ball_x and ball_y are real numbers on the interval [0,1]. The lines x=0, y=0, and y=1 are walls; the ball bounces off a wall whenever it hits. The line x=1 is defended by your paddle.
        # self.ball_x = bx
        # self.ball_y = by
        # #The absolute value of velocity_x is at least 0.03, which guarantees that the ball is moving either left or right at a reasonable speed.
        # self.velocity_x = vx
        # self.velocity_y = vy
        # #paddle_y represents the top of the paddle (the side closer to y=0) and is on the interval [0, 1 - paddle_height], where paddle_height = 0.2, as can be seen in the image above.
        # #(The x-coordinate of the paddle is always paddle_x=1, so you do not need to include this variable as part of the state definition).
        # self.paddle_y = py

# class pongAgent():
#     def __init__(self):
#         #move paddle up, down, or not at all
#         self.possibleActions = [-0.04,0,0.04]
#         #-1 for when ball passes pa3dle, +1 for rebound, 0 otherwise
#         self.possibleRewards = [-1,0,1]
#         self.initialState = pongState(0.5, 0.5, 0.03, 0.01, 0.5 - paddle_height / 2)

class PongPlayer():
    def __init__(self):
        self.currState = self.discretizeLocs(pongState(0.5, 0.5, 0.03, 0.01, 0.5 - paddle_height / 2))
        self.action = 'none'
        self.reward = 0
        self.q = {}
        self.N = {}
        self.rebounded = False
        self.epsilon = 0.2
        for ballx in range(12):
            for bally in range(12):
                for velx in [-1.0,0.0,1.0]:
                    for vely in [-1.0,1.0]:
                        for paddleloc in range(12):
                            ps = pongState(ballx,bally,velx,vely,paddleloc)
                            for action in posActs:
                                #action 0 is nonmobile, 1 is up, 2 is down
                                self.q[(ps,action)] = 0.00
                                self.N[(ps,action)] = 0.00

    #takes current state variable st
    def getNextAction(self,st):
        if st.ball_x == 11:
            #if self.rebounded:
            #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            #print("OH NO, A TRAVESTY has BEfALLEN mE PlEAse EnD mY FeeEBle ExISTEnce")
            self.q[(st,'none')] = self.getReward(st)
            self.rebounded = False
        if True:
            self.N[(self.currState,self.action)] += 1
            nextBest = self.getBestQ(st)
            #print("currstate is ",self.currState)
            #print("and next state should be ", st)
            self.q[(self.currState,self.action)] += self.getAlpha(self.N[(self.currState,self.action)])*(self.reward + GAMMA * nextBest - self.q[(self.currState,self.action)])
            self.currState = st
            self.action = self.getBestNextAction(st)
            self.reward = self.getReward(st)
        return self.action


    def getBestQ(self,s):
        qlist = []
        for action in posActs:
            qlist.append(self.q[(s,action)])
        bestval = max(qlist)
        return bestval

    def getAlpha(self,n):
        #constant c
        return (BIGC/(BIGC+n))

    def getBestNextAction(self,s):
        x = random.random()
        if x <= self.epsilon:
            #print("random choice used")
            return random.choice(posActs)
        else:
            actionlist = []
            for action in posActs:
                e = self.explFunction(s,action)
                actionlist.append(e)
            return posActs[actionlist.index(max(actionlist))]

    def explFunction(self,s,a):
        ret = 1 if self.N[(s,a)] < BIGN else self.q[(s,a)]
        return ret

    def getReward(self,s):
        if self.rebounded is True:
            #print(" REWARD HAS BEEN DISPENSED, HURRAH")
            return 1
        if s.ball_x >= 11 and s.ball_y != s.paddle_y:
#            print("YES I HaveE bEn PuNIShEd")
            return -1
        else:
            return 0

    def discretizeLocs(self,s):
        bx,by,vx,vy,py = s
        newbx = math.floor(bx * 12)
        newby = math.floor(by * 12)
        newvx = float(np.sign(vx))
        newvy = float(np.sign(vy))
        newpy = 11 if (py == 1 - paddle_height) else math.floor(12 * py / (1 - paddle_height))
        return pongState(newbx,newby,newvx,newvy,newpy)

    def printQ(self):
         for x in self.q:
             if self.q.get(x) != 0.0: print(self.q.get(x))

n = pongState(ball_x =0, ball_y=0,vel_x = 0, vel_y = 0, paddle_y = 0)
#print(de.nextState.ball_x)
