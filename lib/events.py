import functools

class Event(object):
    def __init__(self):
        self.callbacks = {}
    def register(self, callback, key=None):
        if key is None:
            key=callback
        assert key not in self.callbacks
        self.callbacks[key] = callback
    def unregister(self, key):
        del self.callbacks[key]
    def __call__(self, *args, **kw):
        for callback in self.callbacks.values():
            callback(*args, **kw)

HANDLER_PREFIX = 'handle'
EVENT_PREFIX = 'event'
SEP = '__'
            
class SubHandler(object):
    def __init__(self, outer, prefix, *innerid):
        self.outer = outer
        self.prefix = prefix
        self.innerid = innerid
    def handler(self, eventname):
        subhandler_name = SEP.join([self.prefix, eventname])
        subhandler = getattr(self.outer, subhandler_name)
        return functools.partial(subhandler, *self.innerid)
    def __getattr__(self, attr):
        parts = attr.split(SEP)
        if len(parts) == 2:
            prefix, eventname = parts
            if HANDLER_PREFIX == prefix:
                return self.handler(eventname)
        sup = super(SubHandler, self)
        return getattr(sup, attr)

def register_event_group(handler, obj, event_names):
    for name in event_names:
        ename = SEP.join([EVENT_PREFIX, name])
        event = getattr(obj, ename)
        hname = SEP.join([HANDLER_PREFIX, name])
        hand = getattr(handler, hname)
        event.register(hand)
