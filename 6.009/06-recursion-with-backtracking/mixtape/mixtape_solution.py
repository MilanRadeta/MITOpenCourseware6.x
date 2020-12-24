# No imports!

# recursive version that works by solving small subproblems and then combining
# the results together as we work our way back up the tree
def mixtape(songs, target_duration):
    """
    Given a dictionary of songs (mapping titles to durations), as well as a
    total target duration, return a set of song titles such that the sum of
    those songs' durations equals the target_duration.

    If no such set exists, return None instead.

    >>> songs = {'A': 5, 'B': 10, 'C': 6, 'D': 2}
    >>> mixtape(songs, 11) == {'A', 'C'}
    True
    >>> mixtape(songs, 1000) == None
    True
    >>> mixtape(songs, 21) == {'A', 'B', 'C'}
    True
    """
    if target_duration == 0:
        return set()
    elif target_duration < 0:
        return None

    for song, duration in songs.items():
        rec_mixtape = mixtape({k:v for k,v in songs.items() if song != k},
                              target_duration - duration)
        if rec_mixtape is not None:
            return rec_mixtape | {song}
    return None


# recursive version that works by building up an answer as we move farther down
# the tree.
def mixtape(songs, target_duration, sofar=None):
    """
    Given a dictionary of songs (mapping titles to durations), as well as a
    total target duration, return a set of song titles such that the sum of
    those songs' durations equals the target_duration.

    If no such set exists, return None instead.

    >>> songs = {'A': 5, 'B': 10, 'C': 6, 'D': 2}
    >>> mixtape(songs, 11) == {'A', 'C'}
    True
    >>> mixtape(songs, 1000) == None
    True
    >>> mixtape(songs, 21) == {'A', 'B', 'C'}
    True
    """
    if sofar is None:
        sofar = set()

    duration = sum(songs[i] for i in sofar) # total duration so far
    if duration == target_duration:
        return sofar
    if duration > target_duration:
        return None

    for song, duration in songs.items():
        if song not in sofar:
            rec_result = mixtape(songs, target_duration, sofar | {song})
            if rec_result is not None:
                return rec_result
    return None


# iterative version, implemented using an agenda (note that we could improve
# efficiency by representing mixtapes as frozensets and keeping a visited set
# to avoid considering the same combination of songs multiple times)
def mixtape(songs, target_duration):
    """
    Given a dictionary of songs (mapping titles to durations), as well as a
    total target duration, return a set of song titles such that the sum of
    those songs' durations equals the target_duration.

    If no such set exists, return None instead.

    >>> songs = {'A': 5, 'B': 10, 'C': 6, 'D': 2}
    >>> mixtape(songs, 11) == {'A', 'C'}
    True
    >>> mixtape(songs, 1000) == None
    True
    >>> mixtape(songs, 21) == {'A', 'B', 'C'}
    True
    """
    agenda = [set()]
    while agenda:
        this_mixtape = agenda.pop()
        duration = sum(songs[i] for i in this_mixtape)
        if duration == target_duration:
            return this_mixtape
        elif duration > target_duration:
            continue # don't add children, we know this branch is fruitless

        for song in songs:
            if song not in this_mixtape:
                agenda.append(this_mixtape | {song})
    return None


if __name__ == '__main__':
    import doctest
    doctest.testmod()
