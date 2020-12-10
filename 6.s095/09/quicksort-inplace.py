#Programming for the Puzzled -- Srini Devadas
#The Disorganized Handyman
#A recursive sorting algorithm based on pivoting where a pivot is selected
#and the list split into three lists: the first containing elements smaller
#than the pivot, second elements equal to the pivot, and the third containing
#elements greater than the pivot. These sublists are recursively sorted.


#This procedure selects a pivot and partitions the list into 3 sublists
#It only uses one element worth of additional storage for the pivot!
def pivotPartitionClever(lst, start, end):
    pivot = lst[end] 
    limits = [start - 1, end]
    i, j, diff = 0, 1, 1
    count = 0
    loops = 0

    while True: 
        loops += 1
        limits[i] += diff
        if limits[i] == limits[j]:
            break
        
        limit, other_limit = limits[i], limits[j]

        if (lst[limit] - pivot) * diff > 0:
            lst[limit], lst[other_limit] = lst[other_limit], lst[limit]
            i, j = j, i
            diff *= -1
            count += 1

    lst[limits[0]] = pivot 

    return limits[0], count, loops


def quicksort(lst, start=0, end=None):
    if end is None:
        end = len(lst) - 1
    count, count1, count2 = 0, 0, 0
    loops, loops1, loops2 = 0, 0, 0
    if start < end: 
        split, count, loops = pivotPartitionClever(lst, start, end) 
        count1, loops1 = quicksort(lst, start, split - 1)
        count2, loops2 = quicksort(lst, split + 1, end)
    return sum((count, count1, count2)), sum((loops, loops1, loops2))

def quickselect(lst, k, start=0, end=None):
    if end is None:
        end = len(lst) - 1
    if start < end: 
        split, count, loops = pivotPartitionClever(lst, start, end) 
        if k < split:
            return quickselect(lst, k, start, split - 1)
        if k > split:
            return quickselect(lst, k, split + 1, end)
        
    return lst[k]
    
a = [4, 65, 2, -31, 0, 99, 83, 782, 1]
b = [4, 4, 65, 2, -31, 0, 99, 83, -31, 782, 1]
L = list(range(100))    # n(n + 1) // 2
D = list(reversed(L))
R = [0] * 100
R[0] = 29
for i in range(len(R)):
    R[i] = (9679 * R[i-1] + 12637 * i) % 2287 
k = 5

arrs = [a, b, L, D, R]
for arr in arrs:
    print ('Initial list is:', arr)

    kelem = quickselect(arr, k)
    print (f'k-th smallest element for k={k + 1}: {kelem}')

    count, loops = quicksort(arr)
    print ('Sorted list is:', arr)
    print ('Moves performed:', count)
    print ('Loops interated:', loops)


