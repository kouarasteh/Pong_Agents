import numpy as np


def affine_forward (A, W, b):
	cache = (A, W, b)
	Z = np.zeros((n,d))
	n = len(A)
	d = len(W[0])
	d_prime = len(W)

	for i in range(n):
		for j in range(d):
			for k in range(d_prime):
				Z[i][j] += A[i][k] * W[k][j]
			Z[i][j] += b[j]
	return Z, cache


def affine_backward (dZ, cache):
	A = cache[0]
	W = cache[1]
	dA = np.zeros((I,J))
	dW = np.zeros((K,J))
	db = np.zeros(J)
	I = len(dZ)
	K = len(W)
	J = len(W[0])

	for i in range (I):
		for k in range(K):
			for j in range(J):
				dA[i][k] += dZ[i][j] * W[k][j]

	for k in range(K):
		for j in range(J):
			for i in range(I):
				dW[k][j] += A[i][k] * dZ[i][j]

	for j in range(J):
		for i in range(I):
			db[j] += dZ[i][j]

	return dA, dW, db


def ReLU_forward (Z):
	cache = Z
	r = Z.shape
	c = r

	for i in range(r):
		for j in range(c):
			reLU = max(0, Z[i][j])
			Z[i][j] = reLU
	return Z, cache


def ReLU_backward (dA, cache):
	dZ = dA
	r = dA.shape
	c = r

	for i in range(r):
		for j in range(c):
			reLU = max(0, dA[i][j])
			dZ[i][j] = reLU
	return dZ


def cross_entropy (F, y, n):
	I = len(F)
	J = len(F[0])
	C = 3
	dF = np.zeros((I,J))
	loss = 0
	for i in range(I):
		Y = y[i]
		middle_sum = 0
		for k in range(C):
			middle_sum += np.exp(F[i][k])
		middle_sum = np.log(middle_sum)
		loss += F[i][Y] - middle_sum
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
