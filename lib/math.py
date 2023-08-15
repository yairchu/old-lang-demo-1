def distance(a, b):
    return sum((ax-bx)**2 for ax, bx in zip(a, b))**.5
