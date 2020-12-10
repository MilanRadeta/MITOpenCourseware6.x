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

    while True: 
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

    return limits[0], count


def quicksort(lst, start, end):
    count = 0
    if start < end: 
        split, count = pivotPartitionClever(lst, start, end) 
        count += quicksort(lst, start, split - 1)
        count += quicksort(lst, split + 1, end)
    return count
    
a = [4, 65, 2, -31, 0, 99, 83, 782, 1]
b = [4, 4, 65, 2, -31, 0, 99, 83, -31, 782, 1]

arrs = [a,b]
for arr in arrs:
    print ('Initial list is:', arr)
    count = quicksort(arr, 0, len(arr) - 1)
    print ('Sorted list is:', arr)
    print ('Moves needed:', count)


