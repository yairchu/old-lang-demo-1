def iterfeeder(it):
    tosend = [None]
    def setsend(x):
        if tosend:
            raise ValueError("cannot send more than one value per iteration")
        tosend.append(x)
    while True:
        try:
            r = it.send(tosend[0])
        except StopIteration:
            break
        tosend = []
        # This will call the user
        # He must call setsend
        yield setsend, r
        if not tosend:
           raise ValueError("must send value") 
