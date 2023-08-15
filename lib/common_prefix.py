import itertools

def common_prefix(ita, itb):
    for a, b in itertools.izip(ita, itb):
        if a == b:
            yield a
        else:
            break
