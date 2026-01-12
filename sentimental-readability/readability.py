text = input("Text: ")
t_len = len(text)


def letter_count(text: str) -> int:
    """
    Use a generator expression for efficiency:
        yields True/False for each char, then sums them (True=1, False=0)

v1.0
    count = 0
    for c in s:
        if c.isalpha():
            count += 1
    return count
    """
    return sum(c.isalpha() for c in text)
# [Generator expression]
# Syntax: (expression for item in iterable)
#     means "for each item in iterable, evaluate expression and yield the result."
# It's like saying: "Generate c.isalpha() for each c in text."


def word_count(text: str) -> int:
    word_list = text.strip().split()
    return len(word_list)
# str.strip(chars="abc")
#     Returns a copy of the string with the leading and trailing characters removed.
#     Stripping whitespaces if no argument is given.
# str.split(sep='c')
#     Returns a list of the words in the string, using sep as the separator.
#   sep should be a character or an exact string, not a set of characters as separators.
#     Uses whitespaces as separators if not given.


def setence_count(text: str) -> int:
    """
v1.0
    setence_list = text.strip().split('.!?')
    return len(setence_list)
    """
    return sum(1 for c in text if c in '.!?')


L = letter_count(text) / word_count(text) * 100
S = setence_count(text) / word_count(text) * 100
grade = round(0.0588 * L - 0.296 * S - 15.8)

if grade < 1:
    print("Before Grade 1")
elif grade >= 16:
    print("Grade 16+")
else:
    print(f"Grade {grade}")
