t = int(input())
for i in range(t):
	size = int(input())
	towers = list(map(int,input().strip().split()))
	jumpTo = size
	for j in range(size-1,-1,-1):
		if towers[j] >= jumpTo-j:
			jumpTo = j
	if jumpTo == 0:
		print("True")
	else:
		print("False")