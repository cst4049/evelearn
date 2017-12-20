

# https://pypi.python.org/pypi/Distance/
# https://github.com/doukremt/distance
# pip install distance

import distance


def levenshtein(seq1,seq2):
    """
    >>> levenshtein("lenvestein", "levenshtein")
    3
    >>> levenshtein(["aa","ab","ac"], ["ab","ac","ad"])
    2
    >>> sent1 = ['the', 'quick', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy', 'dog']
    >>> sent2 = ['the', 'lazy', 'fox', 'jumps', 'over', 'the', 'crazy', 'dog']
    >>> distance.levenshtein(sent1, sent2)
    3

    :param seq1:
    :param seq2:
    :return:
    """
    return distance.levenshtein(seq1,seq2)

def hamming(seq1,seq2):
    """
    >>> hamming("hamming", "hamning")
    1
    >>> hamming(["aa","ac","ad","\\n"], ["ab","ac","ad","\\r"])
    2


    :param seq:
    :param seq2:
    :return:
    """
    return distance.hamming(seq1,seq2)

if __name__ == "__main__":
    import doctest

    doctest.testmod()