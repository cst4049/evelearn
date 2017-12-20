
# https://www.expobrain.net/2013/07/29/hamming-weights-python-implementation/
# https://stackoverflow.com/questions/407587/python-set-bits-count-popcount
# Counting the number of 1’s in a binary representation of a number (aka Hamming weight aka popcount when binary numbers are involved)
# 计算hamming距离

def _count_int_A(i):
    """
    >>> _count_int_A(0b0101110001011100)
    8
    >>> _count_int_A(10000000000000000000000000000000000000000000000000000000000000000000000000000000000000)
    94
    """
    return bin(i).count('1')



def _count_int_B(i):
    """
    >>> _count_int_B(0b0101110001011100)
    8
    >>> _count_int_B(10000000000000000000000000000000000000000000000000000000000000000000000000000000000000)
    94
    """
    s = 0
    while i > 0:
        i &= i - 1
        s += 1
    return s

def _count_int_C(x):
    """
    >>> _count_int_C(0b0101110001011100)
    8
    >>> _count_int_C(10000000000000000000000000000000000000000000000000000000000000000000000000000000000000)
    94

    python中int可以无限长，这里的实现限定了长度
    """
    x -= (x >> 1) & 0x5555555555555555
    x = (x & 0x3333333333333333) + ((x >> 2) & 0x3333333333333333)
    x = (x + (x >> 4)) & 0x0f0f0f0f0f0f0f0f
    return ((x * 0x0101010101010101) & 0xffffffffffffffff ) >> 56

def _count_int_D(i):
    """
    >>> _count_int_D(0b0101110001011100)
    8
    >>> _count_int_D(10000000000000000000000000000000000000000000000000000000000000000000000000000000000000)
    94
    """
    return sum( b == '1' for b in bin(i)[2:])


def _count_int_E(i):
    """
    >>> _count_int_E(0b0101110001011100)
    8
    >>> _count_int_E(10000000000000000000000000000000000000000000000000000000000000000000000000000000000000)
    94
    """
    p = lambda n: n and 1 + p(n & (n - 1))
    return p(i)


if __name__ == '__main__':
    from timeit import timeit

    i = 0b0101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100010111000101110001011100
    for k,f in enumerate([_count_int_A,_count_int_B,_count_int_C,_count_int_D,_count_int_E]):
        print('1000 * {:<20}'.format(f.__name__), timeit(lambda: f(i), number=1000))
