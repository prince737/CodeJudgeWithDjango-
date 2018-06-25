import math as m

def prime(n):
	if a%2==0 or a%3==0:
		return("Not Prime")
	for i in range(5,int(m.sqrt(n))):
		if(a%i==0):
			return("Not Prime")
	return("Prime")

a=int(input())
print(prime(a))
#160479503