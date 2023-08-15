from collections import defaultdict
from itertools import count

# l33t
numid = defaultdict(count().__next__).__getitem__
