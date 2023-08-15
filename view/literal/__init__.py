from . import cls
from model import compute, class_fields
from model.pyapi import nf_getattr, nf_hasattr

def linked_style(path, subwidget_style):
    root_widget = subwidget_style.root_widget
    if root_widget is None:
        return None
    clspath = root_widget.path
    klass = clspath[-1].cls
    links = nf_getattr(klass, class_fields.links)
    if links is None:
        return None
    subpath = path[len(clspath):]
    if subpath not in links:
        return None
    srcpath = links[subpath]
    fullsrcpath = clspath + srcpath
    srcfield = srcpath[0]
    if root_widget.field_filter(srcfield):
        # Its already being displayed by ourwidget, lets not duplicate
        # things in the display, show a LocationBar instead.
        from view.Browser import LocationBar
        srckey = path + ('link',)
        return LocationBar(srckey, srcpath, subwidget_style, srckey)
    result = subwidget_style(clspath + (srcfield, ))
    if len(srcpath) > 1:
        mark = result.get_path(fullsrcpath)
        mark.add_state('mark')
    return result

def clamped_style(path, subwidget_style):
    root_widget = subwidget_style.root_widget
    if root_widget is None:
        return None
    clspath = root_widget.path
    klass = clspath[-1].cls
    subpath = path[len(clspath):]
    if len(subpath) > 1:
        return cls.BriefClassEdit(path, subwidget_style)    

def embed_style(path, subwidget_style):
    klass = path[-1].cls
    root_widget = subwidget_style.root_widget
    if root_widget is not None:
        # Its x.y in the outwidget, so maybe we can use a format
        format = nf_getattr(klass, class_fields.format)
        if format is not None:
            # TODO: Separating (key, path) maybe was a bad idea, now
            # need to guess the path of the src
            return cls.FormatEdit(format, path, subwidget_style)
        viewer = cls.ClassPublicEdit
    elif nf_hasattr(klass, class_fields.links):
        viewer = cls.ClassEdit
    else:
        viewer = cls.BaseClassEdit
    return viewer(path, subwidget_style)

from view.styles import Style
import view.default
class LiteralStyle(Style):
    widget_for_funcs = [
        linked_style,
        view.default.widget_for,
        clamped_style,
        embed_style]
    def __init__(self):
        self.root_widget = None
literal_style = LiteralStyle()
