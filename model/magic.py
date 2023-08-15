from .compute import compute, base_compute
from .field import ConstField, PublicField
from .pyapi import nf_setattr
from .metaclass import base_metaclass
from . import class_fields

magic_metaclass_field = ConstField(
    {'label': 'metaclass of magic'}, base_metaclass)
magic_metaclass = (magic_metaclass_field, )
nf_setattr(magic_metaclass, class_fields.fields,
           [class_fields.fields,
            class_fields.computer,
            class_fields.format
            ])

class MagicComputer(object):
    def __init__(self, pycls):
        self.pycls = pycls
        
    def __call__(self, path, subpath):
        if not subpath:
            return None
        [outfield] = subpath
        if outfield not in self.pycls.outputs:
            return base_compute(path, subpath)
        outindex = self.pycls.outputs.index(outfield)
        invals = []
        for infield in self.pycls.inputs:
            inpath = path + (infield,)
            val = compute(inpath)
            invals.append(val)
        if None in invals:
            return None
        outvals = self.pycls.compute(*invals)
        return outvals[outindex]

def magic_class(pycls):
    field = ConstField(pycls.meta, magic_metaclass)
    path = (field, )
    field.value = {}
    fields = []
    fields.extend(getattr(pycls, 'inputs', []))
    fields.extend(getattr(pycls, 'outputs', []))
    nf_setattr(path, class_fields.fields, fields)
    format = getattr(pycls, 'format', {})
    nf_setattr(path, class_fields.format, format)
    if hasattr(pycls, 'compute'):
        nf_setattr(path, class_fields.computer, MagicComputer(pycls))
    return path
