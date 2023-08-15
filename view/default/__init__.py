from NumberEdit import NumberEdit

import builtins

class_viewer = {
    builtins.nfnumber : NumberEdit,
}

def widget_for(path, subwidget_style):
    """obj is an instance or an (field, instance)"""
    cls = path[-1].cls
    viewer = class_viewer.get(cls, None)
    if viewer is None:
        return None
    return viewer(path, subwidget_style)
