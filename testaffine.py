import dl_helpers as dl
import numpy as np
#A,W,b,Z,dZ,dA,dW,db
A= []
W= []
b = []
Z = []
dZ = []
dA = []
dW = []
db = []
with open('testaffine.txt') as f:
    for x in range(10):
        A.append(f.readline().split())
    f.readline()
    for x in range(8):
        W.append(f.readline().split())
    f.readline()
    b = f.readline().split()
    f.readline()
    for x in range(10):
        Z.append(f.readline().split())
    f.readline()
    for x in range(10):
        dZ.append(f.readline().split())
    f.readline()
    for x in range(10):
        dA.append(f.readline().split())
    f.readline()
    for x in range(8):
        dW.append(f.readline().split())
    f.readline()
    db = f.readline().split()

A= np.array(A).astype(float)
W= np.array(W).astype(float)
b = np.array(b).astype(float)
Z = np.array(Z).astype(float)
dZ = np.array(dZ).astype(float)
dA = np.array(dA).astype(float)
dW = np.array(dW).astype(float)
db = np.array(db).astype(float)

newZ,cache = dl.affine_forward(A,W,b)
print(newZ -Z)

newdA,newdW, newdb = dl.affine_backward(dZ,(A,W))

print(newdA - dA)
print(newdW - dW)
print(newdb - db)
