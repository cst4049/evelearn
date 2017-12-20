
# https://pypi.python.org/pypi/simhash
# https://github.com/leonsim/simhash
# https://leons.im/posts/a-python-implementation-of-simhash-algorithm/
# pip install simhash

from simhash import Simhash
import mmh3

def simhash(realword):
    """
    次序不影响 simhash的结果
    >>> simhash(["aaa","bbb"])
    '0b11001010110100010010101000000100101010001110000000001000'
    >>> simhash(["bbb","aaa"])
    '0b11001010110100010010101000000100101010001110000000001000'

    simhash
    """
    code = Simhash(realword,hashfunc=lambda x: mmh3.hash64(x)[0]).value
    return code