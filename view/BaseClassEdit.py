from .Widget import Widget
from .WidgetList import WidgetList
from .textedit import FieldLabelEdit
from model import Field, class_fields, compute
from model.pyapi import nf_getattr

class SubinstanceEdit(WidgetList):
    dimension = WidgetList.Vertical
    header_first = True
    header_size = 30
    def __init__(self, path, subwidget_style):
        super(SubinstanceEdit, self).__init__(path, subwidget_style)
        self.path = path
        for i in [True, False]:
            if i == self.header_first:
                self.create_key_widget(path + ('key',), path)
            else:
                self.create_value_widget(path)

    def get_path(self, path):
        if path == self.path:
            return self
    
    def create_key_widget(self, key, path):
        field = path[-1]
        self.subwidgets_sizes['key'] = self.header_size
        self.key_widget = FieldLabelEdit(
            field, key, self.subwidget_style)
        self.add_subwidget('key', self.key_widget)

    def create_value_widget(self, path):
        self.value_widget = self.subwidget_style(path)
        self.add_subwidget('value', self.value_widget)

class BaseClassEdit(object):
    subinstance_style = SubinstanceEdit
    def __init__(self, path):
        self.path = path
    def create_subwidget(self, field):
        style = self.subwidget_style
        subinstance = self.path + (field, )
        return self.subinstance_style(subinstance, style)
    def field_filter(self, field):
        return True
    def sync_fields(self):
        cls = self.path[-1].cls
        fields = nf_getattr(cls, class_fields.fields)
        for field in fields:
            if not self.field_filter(field):
                continue
            if field in self.subwidgets:
                continue
            widget = self.create_subwidget(field)
            self.add_subwidget(field, widget)
        for field in list(self.subwidgets.keys()):
            if field in fields or not isinstance(field, Field):
                continue
            self.remove_subwidget(field)
    def node_rect(self, node):
        if len(node) == 1:
            return self.anim_rects.get(node[0])
        siwidget = self.subwidgets[node[0]]
        si_rect = self.anim_rects.get(node[0])
        subwidget = siwidget.subwidgets['value']
        outer_rect = siwidget.anim_rects.get('value')
        inner_rect = subwidget.node_rect(node[1:])
        if None in [si_rect, outer_rect, inner_rect]:
            return None
        return inner_rect.move(outer_rect.topleft).move(si_rect.topleft)
