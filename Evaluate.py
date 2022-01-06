# FUNCTION: Evaluation index
import math

# function: Root Mean Squard Error
def RMSE(truth,test):
    n=len(truth)
    s=sum([(truth[i]-test[i])**2 for i in range(0,n)])

    return math.sqrt(s/n)

# function: Mean Square Error
def MSE(truth,test):
    n = len(truth)
    s = sum([(truth[i] - test[i]) ** 2 for i in range(0, n)])

    return s/n
