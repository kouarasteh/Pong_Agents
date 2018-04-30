import numpy as np
import dl_helpers as help
from random import shuffle


class dl_pong:

    def __init__ (self):
        # read in data from .txt file
        with open("expert_policy.txt") as text_file:
            self.dataset = [line.split() for line in text_file]
        self.floatConvert()

        self.weights = 0
        self.bias = np.zeros(256)


    # shuffles dataset after each epoch
    def shuffleDataset (self):
        shuffle(self.dataset)


    # converts input dataset from string into floating point
    def floatConvert (self):
        for i in range(len(self.dataset)):
            for j in range(6):
                self.dataset[i][j] = float(self.dataset[i][j])




p1 = dl_pong()
print(p1.dataset[0])
p1.shuffleDataset()
print(p1.dataset[0])
