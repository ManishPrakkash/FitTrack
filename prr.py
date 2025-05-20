#transpose of the matrix
import numpy
a=numpy.array([[1,2,3],[4,5,6]])
print(a)
b=a.transpose()
print(b)
#sum in row wise
print(a.sum(axis=1))
#sum in column wise
print(a.sum(axis=0))