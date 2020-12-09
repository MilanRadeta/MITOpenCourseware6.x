#Programming for the Puzzled -- Srini Devadas
#Please Do Break the Crystal
#This is an interactive procedure that given n floors and d balls determines
#what floors to drop the balls from to minimize the worst-case number of
#drops required to determine the hardness coefficient of the crystal.
#The hardness coefficient will range from 0 (breaks at Floor 1) or n (does not
#break at n.
def howHardIsTheCrystal(n, d):

    #First determine the radix r
    r = 1
    while (r**d <= n):
        r = r + 1
    print('Radix chosen is', r)
    
    old_d = d
    #See if you can reduce d
    while (r**d > n):
        d -= 1
    d += 1
    if d < old_d:
        print ('Using only', d, 'balls')

    numDrops = 0
    floorNoBreak = [0] * d
    broken_balls = 0
    min = 0
    max = n
    for i in range(d):
        #Begin phase i
        for j in range(r-1):
            #increment ith digit of representation
            floorNoBreak[i] += 1
            Floor = convertToDecimal(r, d, floorNoBreak)
            #Make sure you aren't higher than the highest floor
            if Floor > n:
                floorNoBreak[i] -= 1
                break
            print('Considering interval [%d,%d]' % (min, max))
            print ('Drop ball', broken_balls + 1, 'from Floor', Floor)
            yes = input('Did the ball break (yes/no)?:').lower()
            numDrops += 1
            if yes in ('yes', 'y'):
                floorNoBreak[i] -= 1
                broken_balls += 1
                max = Floor - 1
                break
            min = Floor + 1


    hardness = convertToDecimal(r, d, floorNoBreak)
    print('Hardness coefficient is', hardness)
    print('Total number of drops is', numDrops)
    print('Total number of broken balls', broken_balls)

    return

def convertToDecimal(r, d, rep):
    number = 0
    for i in range(d-1):
        number += rep[i]
        number *= r
    number += rep[-1]

    return number

howHardIsTheCrystal(128, 6)
