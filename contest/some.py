# Complete the calculateCost function below.
maxi=0
def calculateCost(a, k):
    data = list(range(r))
    n = len(a)
    maxi = findSubsets(arr, n, k, 0, data, 0)
    return maxi
    
def findSubsets(arr, n, r, index, data, i):
	if(index == r):
		global maxi 
		maxi = maxi+max(data)
		return
	if(i >= n):
		return

	data[index] = arr[i]
	findSubsets(arr, n, r, index + 1, data, i + 1)
	findSubsets(arr, n, r, index, data, i + 1)
	return maxi