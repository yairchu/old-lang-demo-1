from view import Browser
from view.WidgetList import WidgetList
from view.textedit import FieldLabelEdit, TextEdit
import model
from model.pyapi import nf_getattr
from model import class_fields
import view.BaseClassEdit

class OuterSubinstanceEdit(view.BaseClassEdit.SubinstanceEdit):
    draw_outline = False
    dimension = WidgetList.Horizontal
    header_size = 200

class BaseClassEdit(view.BaseClassEdit.BaseClassEdit,
                    WidgetList):
    draw_outline = False
    dimension = WidgetList.Vertical
    subinstance_style = OuterSubinstanceEdit
    def __init__(self, path, style):
        if style.root_widget is None:
            style = style.copy()
            style.root_widget = self
        view.BaseClassEdit.BaseClassEdit.__init__(self, path)
        WidgetList.__init__(self, path+('value',), style)
        cls = path[-1].cls
        self.add_subwidget('cls', FieldLabelEdit(cls[-1], path+('class',), style))
    def _draw(self, surface, dest_size):
        self.sync_fields()
        return super(BaseClassEdit, self)._draw(surface, dest_size)

class ClassPublicEdit(BaseClassEdit):
    dimension = WidgetList.Horizontal
    subinstance_style = view.BaseClassEdit.SubinstanceEdit
    def field_filter(self, field):
        return field.is_public()

class ClassEdit(BaseClassEdit):
    def field_filter(self, field):
        cls = self.path[-1].cls
        num_dsts = 0
        links = nf_getattr(cls, class_fields.links)
        for dst, src in links.items():
            if src[:1] == (field, ):
                num_dsts += 1
        return 1 != num_dsts
class FormatTextEdit(TextEdit):
    def __init__(self, text_list, *args, **kwargs):
        super(FormatTextEdit, self).__init__(*args, **kwargs)
        self.text_list = text_list
    def get_text(self):
        return self.text_list[0]
    def set_text(self, text):
        self.text_list[0] = text

class FormatEdit(view.BaseClassEdit.BaseClassEdit,
                 WidgetList):
    """Shows a format"""
    draw_outline = False
    dimension = WidgetList.Horizontal
    subinstance_style = view.BaseClassEdit.SubinstanceEdit

    def __init__(self, format, path, style):
        WidgetList.__init__(self, path+('value',), style)
        view.BaseClassEdit.BaseClassEdit.__init__(self, path)
        for index, item in enumerate(format):
            if isinstance(item, model.Field):
                sub = self.create_subwidget(item)
                self.add_subwidget(item, sub.subwidgets['value'])
            elif isinstance(item, list):
                subkey = ('format', index)
                sub = FormatTextEdit(item, path + subkey, style)
                self.add_subwidget(id(item), sub)
            else:
                assert False
    def _draw(self, surface, dest_size):
        # TODO: sync_fields (with format)
        return super(FormatEdit, self)._draw(surface, dest_size)
    def get_path(self, path):
        if path == self.path:
            return self
        assert path[:len(self.path)] == self.path
        sub = path[len(self.path):]
        first = sub[0]
        return self.subwidgets[first].get_path(path) 
