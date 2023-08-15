import itertools

def common_prefix(ita, itb):
    for a, b in zip(ita, itb):
        if a == b:
            yield a
        else:
            break
