def two_sum(nums, target):
    if len(nums) <= 1:
        return False

    aux_dict = {}
    for i in range(len(nums)):
        if nums[i] in aux_dict:
            return [aux_dict[nums[i]], i]
        else:
            aux_dict[target - nums[i]] = i

t = int(input())
for i in range(t):
    target = int(input())
    leng = int(input())
    nums= list(map(int, input().strip().split()))
    arr = two_sum(nums, target)
    print('%d %d'%(arr[0]+1, arr[1]+1))