import numpy as np
import dl_helpers as help
from random import shuffle

BIGN = 0
batch_size = 128

class dl_pong:

    def __init__ (self):
        # read in data from .txt file
        with open("expert_policy.txt") as text_file:
            self.dataset = [line.split() for line in text_file]
        self.floatConvert()
        self.dataset = np.array(self.dataset)

        self.weights = [(np.random.random((5,256))) for x in range(3)]
        self.bias = [np.zeros(256) for x in range(3)]
        BIGN = len(self.dataset)



    # shuffles dataset after each epoch
    def shuffleDataset (self):
        shuffle(self.dataset)


    # converts input dataset from string into floating point
    def floatConvert (self):
        for i in range(len(self.dataset)):
            for j in range(6):
                self.dataset[i][j] = float(self.dataset[i][j])


    def threeLayerNetwork (self, X, weights, bias, y, test):
        Z1, acache1 = affine_forward(X, weights[0], bias[0])
        A1, rcache1 = ReLU_forward(Z1)
        Z2, acache2 = affine_forward(A1, weights[1], bias[1])
        A2, rcache2 = ReLU_forward(Z2)
        F, acache3 = affine_forward(A2, weights[2], bias[2])

        if test is true:
            classifications = []
            for i in range(batch_size):
                classifications.append(F[i].index(max(F[i])))
            return classifications

        loss, dF = cross_entropy(F, y)
        dA2, dW3, db3 = affine_backward(dF, acache3)
        dZ2 = ReLU_backward(dA2, rcache2)
        dA1, dW2, db2 = affine_backward(dZ2, acache2)
        dZ1 = ReLU_backward(dA1, rcache1)
        dX, dW1, db1 = affine_backward(dZ1, acache1)

        

        return loss


    def minibatch (self, data, epoch):
        for e in range(1, epoch):
            self.shuffleDataset()
            for i in range(1, BIGN/batch_size):
                X, y = self.dataset[:batch_size, :5], self.dataset[:batch_size, 5]
                loss = self.threeLayerNetwork(X, self.weights, self.bias, y, False)


    # centers dataset around 0
    def normalizeData (self):
        col_mean = self.dataset.mean(axis=0)
        col_mean = np.delete(col_mean, 5, 0)

        sd = self.dataset.std(axis=0)
        sd = np.delete(sd, 5, 0)

        for i in range(len(self.dataset)):
            for j in range(5):
                self.dataset[i][j] = (self.dataset[i][j] - col_mean[j]) / sd[j]





p1 = dl_pong()
p1.normalizeData()
