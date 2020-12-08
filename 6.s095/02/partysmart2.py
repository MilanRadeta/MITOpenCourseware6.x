# Programming for the Puzzled -- Srini Devadas
# The Best Time to Party
# Given a list of intervals when celebrities will be at the party
# Output is the time that you want to go the party when the maximum number of
# celebrities are still there.
# Clever algorithm that will work with fractional times

sched = [(6, 8), (6, 12), (6, 7), (7, 8), (7, 10), (8, 9), (8, 10), (9, 12),
         (9, 10), (10, 11), (10, 12), (11, 12)]
sched2 = [(6.0, 8.0), (6.5, 12.0), (6.5, 7.0), (7.0, 8.0), (7.5, 10.0), (8.0, 9.0),
          (8.0, 10.0), (9.0, 12.0), (9.5, 10.0), (10.0, 11.0), (10.0, 12.0), (11.0, 12.0)]
sched3 = [(6, 7), (7, 9), (10, 11), (10, 12), (8, 10), (9, 11), (6, 8),
          (9, 10), (11, 12), (11, 13), (11, 14)]


def bestTimeToPartySmart(schedule, ystart = 0, yend = 24):
    # Convert schedule to list of start times and end times marked as such
    times = []
    for c in schedule:
        times.append((c[0], 'start'))
        times.append((c[1], 'end'))

    # Sort the list of times.
    # Each time is a start or end time of a celebrity sighting.
    sortlist(times)

    maxcount, time = chooseTime(times, ystart, yend)

    # Output best time to party
    print('Best time to attend the party is at', time,
          'o\'clock', ':', maxcount, 'celebrities will be attending!')

def bestTimeToPartyIntersection(schedule):
    # Convert schedule to list of start times and end times marked as such
    best_count = 0
    best_time = None
    for t in schedule:
        if t == schedule[0]:
            continue

        count = 1
        for t2 in schedule:
            if t != t2 and t2[0] <= t[0] < t2[1]:
                count += 1
        
        if count > best_count:
            best_time = t[0]
            best_count = count

    # Output best time to party
    print('Best time to attend the party is at', best_time,
          'o\'clock', ':', best_count, 'celebrities will be attending!')


# Sort the elements of tlist in ascending order
# Sorting is based on the value of the element tuple (both items!)
# The original code had a bug in that it did not look at the second
# item of each tuple and ensure that (x, 'end') of one interval
# is sorted before (x, 'start') of a different tuple.
def sortlist(tlist):
    for i in range(len(tlist)-1):
        for j in range(i, len(tlist)):
            # Sort based on first item of tuple
            if tlist[i][0] > tlist[j][0] or \
               (tlist[i][0] == tlist[j][0] and
                    tlist[i][1] > tlist[j][1]):
                tlist[i], tlist[j] = tlist[j], tlist[i]

def chooseTime(times, ystart = 0, yend = 24):

    rcount = 0
    maxcount = 0
    time = 0

    # Range through the times computing a running count of celebrities
    for t in times:
        rcount += 1 if t[1] == 'start' else -1
        if rcount > maxcount and ystart <= t[0] < yend:
            maxcount = rcount
            time = t[0]

    return maxcount, time


bestTimeToPartySmart(sched)
bestTimeToPartySmart(sched2)
bestTimeToPartySmart(sched3)
bestTimeToPartySmart(sched,  9, 10)
bestTimeToPartySmart(sched2, 9, 10)
bestTimeToPartySmart(sched3, 9, 10)
bestTimeToPartyIntersection(sched)
bestTimeToPartyIntersection(sched2)
bestTimeToPartyIntersection(sched3)
