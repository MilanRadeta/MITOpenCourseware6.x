# NO ADDITIONAL IMPORTS!
from text_tokenize import tokenize_sentences


class Trie:
    def __init__(self):
        self.value = None
        self.children = {}
        self.type = None


    def __setitem__(self, key, value):
        """
        Add a key with the given value to the trie, or reassign the associated
        value if it is already present in the trie.  Assume that key is an
        immutable ordered sequence.  Raise a TypeError if the given key is of
        the wrong type.
        """
        if not (isinstance(key, tuple) or isinstance(key, str)):
            raise TypeError(type(key))

        if self.type is None:
            self.type = type(key)
        elif self.type != type(key):
            raise TypeError(type(key))

        if len(key) > 0:
            self.children.setdefault(key[0:1], Trie())[key[1:]] = value
        else:
            self.value = value

    def __getitem__(self, key):
        """
        Return the value for the specified prefix.  If the given key is not in
        the trie, raise a KeyError.  If the given key is of the wrong type,
        raise a TypeError.
        """
        if self.type is not None and self.type != type(key):
            raise TypeError(type(key))

        
        if len(key) > 0:
            try:
                return self.children[key[0:1]][key[1:]]
            except KeyError:
                raise KeyError(key)
        else:
            if self.value is None:
                raise KeyError(key)
            return self.value

    def __delitem__(self, key):
        """
        Delete the given key from the trie if it exists. If the given key is not in
        the trie, raise a KeyError.  If the given key is of the wrong type,
        raise a TypeError.
        """
        if self.type is not None and self.type != type(key):
            raise TypeError(type(key))
        
        if key in self:
            self[key] = None
        else:
            raise KeyError(key)

    def __contains__(self, key):
        """
        Is key a key in the trie? return True or False.
        """
        try:
            return self[key] and True
        except KeyError:
            return False

    def __iter__(self):
        """
        Generator of (key, value) pairs for all keys/values in this trie and
        its children.  Must be a generator!
        """
        for key, trie in self.children.items():
            if trie.value is not None:
                yield (key, trie.value)
            for sub, val in trie:
                yield (key + sub, val)


def make_word_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    words in the text, and whose values are the number of times the associated
    word appears in the text
    """
    trie = Trie()
    for sentence in tokenize_sentences(text):
        for word in sentence.split():
            if word not in trie:
                trie[word] = 0
            trie[word] += 1
    return trie


def make_phrase_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    sentences in the text (as tuples of individual words) and whose values are
    the number of times the associated sentence appears in the text.
    """
    trie = Trie()
    for sentence in tokenize_sentences(text):
        sentence = tuple(sentence.split())
        if sentence not in trie:
            trie[sentence] = 0
        trie[sentence] += 1
    return trie


def autocomplete(trie, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring elements that start with
    the given prefix.  Include only the top max_count elements if max_count is
    specified, otherwise return all.

    Raise a TypeError if the given prefix is of an inappropriate type for the
    trie.
    """

    if not isinstance(prefix, trie.type):
        raise TypeError
    
    result = []
    for i in range(len(prefix)):
        l = prefix[i:i+1]
        try:
            trie = trie.children[l]
        except:
            return []

    if trie.value is not None:
        result.append((prefix, trie.value))
    for key, val in trie:
        result.append((prefix + key, val))

    result.sort(key=lambda item: item[1], reverse=True)

    result = [key for key, val in result]

    if max_count is None:
        return result
    
    return result[:max_count]


def autocorrect(trie, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.  Include up to
    max_count elements from the autocompletion.  If autocompletion produces
    fewer than max_count elements, include the most-frequently-occurring valid
    edits of the given word as well, up to max_count total elements.
    """
    raise NotImplementedError


def word_filter(trie, pattern):
    """
    Return list of (word, freq) for all words in trie that match pattern.
    pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    """
    raise NotImplementedError


# you can include test cases of your own in the block below.
if __name__ == '__main__':
    pass
