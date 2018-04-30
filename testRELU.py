import dl_helpers as dl
import numpy as np
#A,W,b,Z,dZ,dA,dW,db
Z= []
A = []
dA = []
dZ = []

with open('testRELU.txt') as f:
    for x in range(10):
        Z.append(f.readline().split())
    f.readline()
    for x in range(10):
        A.append(f.readline().split())
    f.readline()
    for x in range(10):
        dA.append(f.readline().split())
    f.readline()
    for x in range(10):
        dZ.append(f.readline().split())

A= np.array(A).astype(float)
Z = np.array(Z).astype(float)
dZ = np.array(dZ).astype(float)
dA = np.array(dA).astype(float)

newZ,cache = dl.ReLU_forward(Z)
print(A -Z)

newdZ = dl.ReLU_backward(dA,cache)
print(newdZ - dZ)
