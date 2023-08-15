from field import ConstField
from pyapi import nf_setattr
import class_fields

base_metaclass_field = ConstField({'label': 'base metaclass'}, None)
base_metaclass = (base_metaclass_field, )
base_metaclass_field.cls = base_metaclass

nf_setattr(base_metaclass, class_fields.fields,
           [class_fields.fields, class_fields.format])

metaclass_field = ConstField({'label': 'nf metaclass'}, base_metaclass)
metaclass = (metaclass_field, )
nf_setattr(metaclass, class_fields.fields, class_fields.all_fields)
