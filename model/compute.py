from .field import PublicField
from . import class_fields

def compute(path):
    path = cut_path_from_last_const(path)
    if (path[0].is_const()
        and all(x.is_public() for x in path[1:])):
        return compute_const(path)
    return sub_compute(path[:1], path[1:])

def cut_path_from_last_const(path):
    cut_index = 0
    for index, field in enumerate(path):
        if field.is_const():
            cut_index = index
    return path[cut_index:]

def compute_const(path):
    val = path[0].value
    if len(path) == 1:
        return val
    else:
        return val.get(path[1:])

def sub_compute(path, subpath):
    cls = path[-1].cls
    computer = compute(cls + (class_fields.computer, ))
    if computer is None:
        computer = cls_compute
    return computer(path, subpath)

def base_compute(path, subpath):
    if not subpath:
        return None
    return sub_compute(path + subpath[:1], subpath[1:])

def cls_compute(path, subpath):
    cls = path[-1].cls
    links = compute(cls + (class_fields.links, ))
    for i in range(len(subpath)):
        prefix, suffix = subpath[:i+1], subpath[i+1:]
        if prefix in links:
            newpath = path + links[prefix]
            return compute(newpath)
    return base_compute(path, subpath)
