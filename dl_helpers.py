import numpy as np


def affine_forward (A, W, b):
	cache = (A, W, b)
	Z = np.matmul(A,W) + b
	return Z, cache


def affine_backward (dZ, cache):
	A = cache[0]
	W = cache[1]
	dA = np.matmul(dZ,np.transpose(W))
	dW = np.matmul(np.transpose(A),dZ)
	db = np.sum(dZ,axis=0)
	return dA, dW, db


def ReLU_forward (Z):
	cache = Z
	Z[np.where(Z<0)] = 0
	return Z, cache


def ReLU_backward (dA, cache):
	dZ = dA
	r = dA.shape
	for i in range(r[0]):
		for j in range(r[1]):
			if cache[i][j] == 0: dZ[i][j] = 0
	return dZ


def cross_entropy (F, y, n):
	I = len(F)
	J = len(F[0])
	C = 3
	dF = np.zeros((I,J))
	loss = np.float64(0)
	for i in range(I):
		middle_sum = 0.00
		for k in range(C):
			middle_sum += np.exp(F[i][k])
		middle_sum = np.log(middle_sum)
		loss += F[i][int(y[i])] - middle_sum
	loss = loss * (-1/n)

	for i in range(I):
		for j in range(J):
			denom = 0
			for k in range(C):
				denom += np.exp(F[i][k])
			indicator = 0
			if (j == y[i]):
				indicator = 1
			dF[i][j] = (indicator - np.exp(F[i][j])/denom) * (-1/n)

	return loss, dF
