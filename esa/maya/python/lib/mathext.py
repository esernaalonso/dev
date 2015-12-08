#######################################
# imports

import math

#######################################
# functionality

###################
# vector functions

def magnitude(v):
	return math.sqrt(sum(v[i]*v[i] for i in range(len(v))))

def add(u, v):
	return [ u[i]+v[i] for i in range(len(u)) ]

def sub(u, v):
	return [ u[i]-v[i] for i in range(len(u)) ]

def dot(u, v):
	return sum(u[i]*v[i] for i in range(len(u)))

def cross(u, v):
	dimension = len(a)
	c = []
	for i in range(dimension):
		c.append(0)
		for j in range(dimension):
			if j != i:
				for k in range(dimension):
					if k != i:
						if k > j:
							c[i] += a[j]*b[k]
						elif k < j:
							c[i] -= a[j]*b[k]
	return c

def normalize(v):
	vmag = magnitude(v)
	return [ v[i]/vmag  for i in range(len(v)) ]

#######################################
# execution

if __name__ == "__main__":
	pass