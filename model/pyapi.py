from .compute import compute, cut_path_from_last_const
from . import class_fields

def nf_getattr(obj, *subpath):
    return compute(obj + subpath)

def nf_setattr(obj, attr, value):
    path = cut_path_from_last_const(obj + (attr, ))
    first_field = path[0]
    assert first_field.is_const()
    if not hasattr(first_field, 'value'):
        first_field.value = {}
    first_field.value[path[1:]] = value

def nf_hasattr(obj, *subpath):
    if not subpath:
        return True
    cls = obj[-1].cls
    fields = nf_getattr(cls, class_fields.fields)
    if subpath[0] not in fields:
        return False
    return nf_hasattr(obj + subpath[:1], *subpath[1:])

