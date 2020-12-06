# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

from os import execlp
import string
import pathlib

### HELPER CODE ###


def load_words(file_name):
    '''
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open(pathlib.Path(
        __file__).parent.absolute().__str__() + "\\story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###


WORDLIST_FILENAME = pathlib.Path(
    __file__).parent.absolute().__str__() + '\\words.txt'


class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object

        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class

        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.

        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()

    def char_to_ord(letter):
        return ord(letter) if isinstance(letter, str) else letter

    def get_in_range_letter(letter, shift, limits):
        min_letter, max_letter = limits
        min_letter = Message.char_to_ord(min_letter)
        max_letter = Message.char_to_ord(max_letter)
        letter = Message.char_to_ord(letter)

        if shift != 0:
            shift //= abs(shift)

        if letter < min_letter or letter > max_letter:
            letter -= (max_letter - min_letter + 1) * shift

        return chr(letter)

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.

        shift (integer): the amount by which to shift every letter of the
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        '''
        result = {}
        for letter in string.ascii_letters:
            new_letter = ord(letter) + shift
            new_letter = Message.get_in_range_letter(
                new_letter, shift,
                ('A', 'Z') if letter.isupper() else ('a', 'z')
            )
            result[letter] = new_letter
        return result

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift

        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        shift_dict = self.build_shift_dict(shift)
        return ''.join([shift_dict[char] if char in shift_dict else char for char in self.message_text])


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object

        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        super().__init__(text)
        self.change_shift(shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class

        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class

        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class

        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other
        attributes determined by shift.

        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object

        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        super().__init__(text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create
        the maximum number of valid words, you may choose any of those shifts
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        max_words = 0
        max_shift = -1
        best_message = None
        for shift in range(ord('Z') - ord('A') + 1):
            words_count = 0
            decrypted_message = self.apply_shift(shift)
            for word in decrypted_message.split():
                if is_word(self.valid_words, word):
                    words_count += 1
            if words_count > max_words:
                max_shift = shift
                max_words = words_count
                best_message = decrypted_message
        return (max_shift, best_message)


if __name__ == '__main__':

    # TODO: WRITE YOUR TEST CASES HERE
    # Example test case (PlaintextMessage)
    plaintext = PlaintextMessage('hello', 2)
    expected = 'jgnnq'
    actual = plaintext.get_message_text_encrypted()
    if expected != actual:
        print('FAILURE')
        print('Expected Output: ', expected)
        print('Actual Output:', actual)
        exit(-1)

    plaintext = PlaintextMessage('Hello, world!', 3)
    expected = 'Khoor, zruog!'
    actual = plaintext.get_message_text_encrypted()
    if expected != actual:
        print('FAILURE')
        print('Expected Output: ', expected)
        print('Actual Output:', actual)
        exit(-1)

    # Example test case (CiphertextMessage)
    ciphertext = CiphertextMessage('jgnnq')
    expected = (24, 'hello')
    actual = ciphertext.decrypt_message()
    if expected != actual:
        print('FAILURE')
        print('Expected Output: ', expected)
        print('Actual Output:', actual)
        exit(-1)

    # Example test case (CiphertextMessage)
    ciphertext = CiphertextMessage('Lipps, asvph!')
    expected = (22, 'Hello, world!')
    actual = ciphertext.decrypt_message()
    if expected != actual:
        print('FAILURE')
        print('Expected Output: ', expected)
        print('Actual Output:', actual)
        exit(-1)

    # TODO: best shift value and unencrypted story
