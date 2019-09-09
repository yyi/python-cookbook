# Example of flattening a nested sequence using subgenerators

from collections.abc import Iterable


def flatten(its, ignore_types=(str, bytes)):
    for i in its:
        if isinstance(i, Iterable) and not isinstance(i, ignore_types):
            yield from flatten(i)
        else:
            yield i


items = [1, 2, [3, 4, [5, 6], 7], 8]

# Produces 1 2 3 4 5 6 7 8
for x in flatten(items):
    print(x)

items = ['Dave', 'Paula', ['Thomas', 'Lewis']]
for x in flatten(items):
    print(x)
