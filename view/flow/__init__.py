from model.pyapi import nf_hasattr
from model import class_fields

def widget_for(path, subwidget_style):
    cls = path[-1].cls
    if nf_hasattr(cls, class_fields.links):
        from .ClassEdit import ClassEdit
        viewer = ClassEdit
    else:
        from .BaseClassEdit import BaseClassEdit
        viewer = BaseClassEdit
    return viewer(path, subwidget_style)
