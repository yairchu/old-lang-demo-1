from view.Widget import Widget
from lib.pygameutils import draw_centered_text

import pygame

class TextEdit(Widget):
    def handle_key__BACKSPACE(self, key_event):
        if key_event.mod & pygame.KMOD_CTRL:
            self.set_text('')
            return True
        self.set_text(self.get_text()[:-1])
        return True
    def handle_anykey(self, key_event):
        if super(TextEdit, self).handle_anykey(key_event):
            return True
        self.set_text(self.get_text() + key_event.unicode)
        return True
    def _draw(self, surface, dest_size):
        text = self.get_text()
        draw_centered_text(surface, text, (0, 0, 0))

class FieldLabelEdit(TextEdit):
    def __init__(self, field, *args, **kwargs):
        super(FieldLabelEdit, self).__init__(*args, **kwargs)
        self.field = field
    def get_text(self):
        return self.field.meta.get('label', '')
    def set_text(self, text):
        self.field.meta['label'] = text
