
from timeit import timeit

a = 'fsffvfdsbbdfvvdavavavavavava'
b = 'fvdaabavvvvvadvdvavavadfsfsdafvvav'

from sc.distance import impl_distance, impl_editdistance

print('1000 * levenshtein of impl_distance:', timeit(lambda: impl_distance.levenshtein(a, b), number=1000))

print('1000 * levenshtein of impl_editdistance:', timeit(lambda: impl_editdistance.levenshtein(a, b), number=1000))