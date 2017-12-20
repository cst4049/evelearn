

# https://pypi.python.org/pypi/editdistance
# https://www.github.com/aflc/editdistance
# pip install editdistance


import editdistance


def levenshtein(seq1,seq2):
    """
    >>> levenshtein("lenvestein", "levenshtein")
    3
    >>> levenshtein(["aa","ab","ac"], ["ab","ac","ad"])
    2
    >>> sent1 = ['the', 'quick', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy', 'dog']
    >>> sent2 = ['the', 'lazy', 'fox', 'jumps', 'over', 'the', 'crazy', 'dog']
    >>> levenshtein(sent1, sent2)
    3

    :param seq1:
    :param seq2:
    :return:
    """
    return editdistance.eval(seq1,seq2)


#
# if __name__ == "__main__":
#     import doctest
#
#     doctest.testmod()