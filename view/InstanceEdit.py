from view.Widget import Widget
from lib.pygameutils import draw_centered_text

class InstanceEdit(Widget):
    def __init__(self, path, subwidget_style):
        super(InstanceEdit, self).__init__(path, subwidget_style)
        self.path = path
        self.key = path+('value',)
    def text(self):
        cls = self.obj.cls
        class_name = cls.meta.get('label')
        return '\n'.join(x for x in [class_name]
                         if x is not None)
    def _draw(self, surface, dest_size):
        text = self.text()
        draw_centered_text(
            surface, text, (0, 0, 0))
    def get_path(self, path):
        if path == self.path:
            return self
