import dl_helpers as dl
import numpy as np
#A,W,b,Z,dZ,dA,dW,db
F= []
y = []
L = []
dF = []

with open('testcrossEntropy.txt') as f:
    for x in range(10):
        F.append(f.readline().split())
    f.readline()
    y = (f.readline().split())
    f.readline()
    L = f.readline()
    f.readline()
    for x in range(10):
        dF.append(f.readline().split())

F= np.array(F).astype(float)
y = np.array(y).astype(float)
L = float(L)
dF = np.array(dF).astype(float)

loss,newdF = dl.cross_entropy(F,y,10)
print(loss - L)
print(newdF - dF)
