from __future__ import division
from model.magic import magic_class
from model.field import PublicField, ConstField
from model.compute import class_fields

# Type declarations:

class _nfnumber(object):
    meta = {'label': 'number'}
nfnumber = magic_class(_nfnumber)

# Func declaratations:

def make_sig(**kwargs):
    trans = dict(_eq='=')
    res = []
    for key, value in kwargs.iteritems():
        label = trans.get(key, key)
        field = PublicField({'label': label}, value)
        res.append(field)
    return res

class _add(object):
    meta = {'label': '+'}
    inputs = make_sig(a=nfnumber, b=nfnumber)
    outputs = make_sig(_eq=nfnumber)
    format = [inputs[0], ['+'], inputs[1], ['='], outputs[0]]
    @staticmethod
    def compute(a, b):
        r = a + b
        return r,
add = magic_class(_add)

class _multiply(object):
    meta = {'label': '*'}
    inputs = make_sig(a=nfnumber, b=nfnumber)
    outputs = make_sig(_eq=nfnumber)
    @staticmethod
    def compute(a, b):
        r = a * b
        return r,
multiply = magic_class(_multiply)
