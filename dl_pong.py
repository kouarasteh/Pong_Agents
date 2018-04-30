import numpy as np
import dl_helpers as dl
import math,pickle,random
batch_size = 128
step_size = 0.1

class dl_pong:

    def __init__ (self):
        # read in data from .txt file
        with open("expert_policy.txt") as text_file:
            self.dataset = [line.split() for line in text_file]
        self.floatConvert()
        self.dataset = np.array(self.dataset)
        self.weights = [np.random.uniform(0,0.01,(5,256)),np.random.uniform(0,0.01,(256,256)),np.random.uniform(0,0.01,(256,3))]
        self.bias = [np.zeros(256),np.zeros(256),np.zeros(3)]
        self.BIGN = len(self.dataset)


    # shuffles dataset after each epoch
    def shuffleDataset (self):
        np.random.shuffle(self.dataset)

    # converts input dataset from string into floating point
    def floatConvert (self):
        for i in range(len(self.dataset)):
            for j in range(6):
                self.dataset[i][j] = float(self.dataset[i][j])


    def threeLayerNetwork (self, X, weights, bias, y, test):
        Z1, acache1 = dl.affine_forward(X, weights[0], bias[0])
        A1, rcache1 = dl.ReLU_forward(Z1)
        Z2, acache2 = dl.affine_forward(A1, weights[1], bias[1])
        A2, rcache2 = dl.ReLU_forward(Z2)
        F, acache3 = dl.affine_forward(A2, weights[2], bias[2])

        if test is True:
            classifications = []
            for i in range(batch_size):
                #print(F[i])
                classifications.append(F[i].argmax())
            return classifications

        loss, dF = dl.cross_entropy(F, y,batch_size)
        dA2, dW3, db3 = dl.affine_backward(dF, acache3)
        dZ2 = dl.ReLU_backward(dA2, rcache2)
        dA1, dW2, db2 = dl.affine_backward(dZ2, acache2)
        dZ1 = dl.ReLU_backward(dA1, rcache1)
        dX, dW1, db1 = dl.affine_backward(dZ1, acache1)
        #print(dF)

        #print(weights[0])
        #print(dW1)
        weights[0] = weights[0] - step_size*dW1
        weights[1] = weights[1] - step_size*dW2
        weights[2] = weights[2] - step_size*dW3

        bias[0] = bias[0] - step_size*db1
        bias[1] = bias[1] - step_size*db2
        bias[2] = bias[2] - step_size*db3


        return loss


    def minibatch (self, data, epoch):
        for e in range(epoch):
            self.shuffleDataset()
            for i in range(1, math.floor(self.BIGN/batch_size)):
                X, y = self.dataset[:batch_size, :5], self.dataset[:batch_size, 5]
                loss = self.threeLayerNetwork(X, self.weights, self.bias, y, False)
            print(e)

    # centers dataset around 0
    def normalizeData (self):
        col_mean = self.dataset.mean(axis=0)
        col_mean = np.delete(col_mean, 5, 0)

        sd = self.dataset.std(axis=0)
        sd = np.delete(sd, 5, 0)

        for i in range(len(self.dataset)):
            for j in range(5):
                self.dataset[i][j] = (self.dataset[i][j] - col_mean[j]) / sd[j]

    def evalModel(self):
        numCorrect = 0
        denom = 0
        for k in range(100):
            self.shuffleDataset()
            #print(self.dataset)
            X, y = self.dataset[:batch_size, :5], self.dataset[:batch_size, 5]
            #print("X",X)
            predictions = self.threeLayerNetwork(X, self.weights, self.bias, y, True)
            for idx in range(len(y)):
                #print(X,y)
                #print("Predicted/Actual: ",predictions[idx],",",y[idx])
                if predictions[idx] == y[idx]:
                    numCorrect += 1
                denom += 1
        print("Correctly guessed: ",numCorrect,"/",denom)

    def writeToFile(self,wfilename, bfilename):
        wfile = open(wfilename,'wb')
        bfile = open(bfilename,'wb')
        pickle.dump(self.weights, wfile)
        pickle.dump(self.bias,bfile)

    def readFromFile(self,wfilename,bfilename):
        wfile = open(wfilename,'rb')
        bfile = open(bfilename,'rb')
        self.weights = pickle.load(wfile)
        self.bias = pickle.load(bfile)

p1 = dl_pong()
p1.readFromFile('weights.txt','biases.txt')
p1.normalizeData()
p1.minibatch(p1.dataset,300)
p1.writeToFile('weights.txt','biases.txt')
p1.evalModel()
