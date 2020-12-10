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

    while True: 
        limits[i] += diff
        if limits[i] == limits[j]:
            break
        
        limit, other_limit = limits[i], limits[j]

        if (lst[limit] - pivot) * diff > 0:
            lst[limit], lst[other_limit] = lst[other_limit], lst[limit]
            i, j = j, i
            diff *= -1

    lst[limits[0]] = pivot 

    return limits[0]


def quicksort(lst, start, end):
    if start < end: 
        split = pivotPartitionClever(lst, start, end) 
        quicksort(lst, start, split - 1)
        quicksort(lst, split + 1, end)
    return
    
a = [4, 65, 2, -31, 0, 99, 83, 782, 1]
print ('Initial list is:', a)
quicksort(a, 0, len(a) - 1)
print ('Sorted list is:', a)

b = [4, 4, 65, 2, -31, 0, 99, 83, -31, 782, 1]

