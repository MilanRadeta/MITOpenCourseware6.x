def is_palindrome(text):
    text = text.lower()
    if len(text) <= 1:
        return True
    
    return text[0] == text[-1] and is_palindrome(text[1:-1])

def is_palindrome_iterative(text):
    text = text.lower()
    i = 0
    j = len(text) - 1
    while i < j:
        if text[i] != text[j]:
            return False
        i += 1
        j -= 1
    return True

print(is_palindrome('kayaK'))
print(is_palindrome('kayyaK'))
print(is_palindrome_iterative('kayaK'))
print(is_palindrome_iterative('kayyaK'))