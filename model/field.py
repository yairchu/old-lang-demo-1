class Field(object):
    def __init__(self, meta, cls):
        self.meta = meta
        self.cls = cls
    def __repr__(self):
        if len(self.meta) == 1 and 'label' in self.meta:
            return '%s(%r)' % (self.__class__.__name__, self.meta['label'])
        return '%s(%r)' % (self.__class__.__name__, self.meta)
    def is_public(self):
        return False
    def is_const(self):
        return False

class PublicField(Field):
   def is_public(self):
       return True

class ConstField(Field):
    def is_const(self):
        return True
