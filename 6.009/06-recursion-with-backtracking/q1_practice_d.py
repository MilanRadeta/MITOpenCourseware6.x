def get_mode(data):
    """
    >>> get_mode([3, 76, 42, 3])
    3
    >>> get_mode([1, 94, 36, 1, 36])
    36
    """
    stats = {}
    for i in data:
        stats[i] = stats.setdefault(i, 0) + 1
    return sorted(stats.items(), key=lambda item: (item[1], item[0]), reverse=True)[0][0]

def find_anagram_groups(words, N):
    """
    >>> find_anagram_groups(["list", "silt", "list"], 3)
    2
    >>> find_anagram_groups(["crate", "word", "filler", "react", "trace"], 2)
    3
    >>> find_anagram_groups(["cat", "act", "tab", "bat", "ten"], 3) == None
    True
    >>> find_anagram_groups(["petal", "tale", "late", "plate"], 2)
    2
    """
    for i in range(N - 1, len(words)):
        group = words[:i + 1]
        letters = sorted(group[-1])
        count = 0
        for word in group:
            if sorted(word) == letters:
                count += 1
                if count == N:
                    return i
    return None

def find_duplicates(stream, init=True, sofar=None):
    """
    >>> find_duplicates(["a", "b", "c", "a"])
    {'a'}
    >>> find_duplicates({"a": "b", "c": ["d", "e"]})
    set()
    >>> find_duplicates((["one"], {"two", ("three", ("one", ("two",)))}))
    {'one', 'two'}
    """
    if sofar is None:
        sofar = {}
    if isinstance(stream, list) or isinstance(stream, tuple) or isinstance(stream, set):
        for elem in stream:
            find_duplicates(elem, False, sofar)
    elif isinstance(stream, dict):
        find_duplicates(set(stream.keys()), False, sofar)
        find_duplicates(tuple(stream.values()), False, sofar)
    else:
        sofar[stream] = sofar.setdefault(stream, 0) + 1
    if init:
        return {key for key in sofar if sofar[key] > 1}
    return sofar



if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags) #runs ALL doctests
