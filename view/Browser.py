from WidgetList import WidgetList
import model
from model.pyapi import nf_getattr
from model import class_fields
from lib.common_prefix import common_prefix

class LocationBar(WidgetList):
    dimension = WidgetList.Horizontal

    draw_outline = False
    def __init__(self, key, path, subwidget_style, suffix=('key',)):
        super(LocationBar, self).__init__(key, subwidget_style)
        self.path = path
        from textedit import FieldLabelEdit
        for i, p in enumerate(path):
            if not isinstance(p, model.Field):
                continue
            subkey = path[:i+1]+suffix
            sub = FieldLabelEdit(p, subkey, subwidget_style)
            self.add_subwidget(path[:i+1], sub)

class Browser(WidgetList):
    dimension = WidgetList.Vertical
    def __init__(self, subwidget_style):
        key = 'browser',
        super(Browser, self).__init__(key, subwidget_style)
        self.stack = []
        self.object_widget = None
        self.location_widget = None
        self.subwidgets_sizes['key'] = 50
        self.clipboard = None
    def _set_sub(self, path):
        for key in self.subwidgets.keys():
            self.remove_subwidget(key)
        self.object_widget = self.subwidget_style(path)
        valpath = []
        for k in path:
            valpath.append(k)
            valpath.append('value')
        valpath = tuple(valpath)
        self.add_subwidget(valpath, self.object_widget)
        lockey = 'location',
        self.location_widget = LocationBar(
            lockey, path, self.subwidget_style)
        self.add_subwidget('key', self.location_widget)
        self.link_src = None
        self.drag_src = False
        self.cursors['keyboard'].set(valpath)
        self.path = path

    def keyboard_cursor_path(self):
        return getattr(self.cursors['keyboard'].final_subwidget(), 'path', None)

    def handle_key__RETURN(self, key_event):
        oldpath = self.stack[-1]
        path = self.keyboard_cursor_path()
        if path is not None:
            return self.enter(path)
    def handle_key__ESCAPE(self, key_event):
        return self.back()
    
    def handle_key__S(self, key_event):
        'set link-source'
        widget = self.cursors['keyboard'].final_subwidget()
        if hasattr(widget, 'path'):
            if self.link_src is not None:
                self.link_src.remove_state('link_src')
            self.link_src = widget
            self.link_src.add_state('link_src')
        
    def handle_key__D(self, key_event):
        'link from link-source to current'
        if self.link_src is None:
            return
        src_path = self.link_src.path
        dst_path = self.keyboard_cursor_path()
        if dst_path is None:
            return
        self.link(src_path, dst_path)

    def handle_key__F(self, key_event):
        'unlink current'
        dst_path = self.keyboard_cursor_path()
        self.unlink(dst_path)
        
    def handle_mouse__left_down(self, event):
        self.drag_src = self.cursors['mouse'].final_subwidget()
        self.drag_src.add_state('drag_src')
        
    def handle_mouse__left_up(self, event):
        drag_src = self.drag_src
        self.drag_src = None
        drag_src.remove_state('drag_src')

        drag_dst = self.cursors['mouse'].final_subwidget()
        if drag_src == drag_dst:
            # Drag to self is select
            self.cursors['keyboard'].copy(self.cursors['mouse'])
            return
        
        src_path = getattr(drag_src, 'path', None)
        if src_path is None:
            return
        dest_path = getattr(drag_dst, 'path', None)
        if dest_path is None:
            return
        self.link(src_path, dest_path)
    
    def handle_key__C(self, key_event):
        'copy'
        self.clipboard = self.keyboard_cursor_path()
    
    def handle_key__V(self, key_event):
        'paste as priVate'
        self.paste(model.Field)
    def handle_key__B(self, key_event):
        'paste as puBlic'
        from model.field import PublicField
        self.paste(PublicField)
    def handle_key__N(self, key_event):
        'paste as coNstant'
        from model.field import ConstField
        self.paste(ConstField)

    def handle_key__BACKSPACE(self, key_event):
        'delete'
        self.delete_selected()
    def handle_key__DELETE(self, key_event):
        'delete'
        self.delete_selected()

    def prehandle_key__TAB(self, key_event):
        from view.styles import styles
        cur_index = styles.index(self.subwidget_style)
        new_style = (styles[cur_index:]+styles[:cur_index])[-1]
        self.subwidget_style = new_style
        self._set_sub(self.stack[-1])

    def delete_selected(self):
        path = self.keyboard_cursor_path()
        if len(path) < 1:
            return
        parent_path = path[:-1]
        cls = parent_path[-1].cls
        field = path[-1]
        cls.remove_field(field)

    def paste(self, fieldtype):
        if self.clipboard is None:
            return
        clipcls = self.clipboard[-1].cls
        field = fieldtype({}, clipcls)
        parentcls = self.path[-1].cls
        parentcls.add_field(field)
    def link(self, src_path, dst_path):
        common_parent_path = tuple(common_prefix(src_path, dst_path))
        common_parent = self.path + common_parent_path
        cls = common_parent[-1].cls
        links = nf_getattr(cls, class_fields.links)
        if links is None:
            return
        cut = len(common_parent_path)
        src_rel_path = src_path[cut:]
        dst_rel_path = dst_path[cut:]
        if not src_rel_path or not dst_rel_path:
            return
        if src_path[-1].cls != dst_path[-1].cls:
            return
        if links.get(src_rel_path) == dst_rel_path:
            return
        links[dst_rel_path] = src_rel_path
        # TODO: THIS IS TEMP HACK
        self._set_sub(self.stack[-1])
    def unlink(self, path):
        for i in range(len(self.path), len(path)):
            subpath = path[:i]
            cls = subpath[-1].cls
            links = nf_getattr(cls, class_fields.links)
            if links is None:
                continue
            if path[i:] in links:
                del links[path[i:]]
        # TODO: THIS IS TEMP HACK
        self._set_sub(self.stack[-1])
    def enter(self, obj):
        self._set_sub(obj)
        self.stack.append(obj)
        return True
    def back(self):
        if len(self.stack) <= 1:
            return False
        self.stack.pop()
        self._set_sub(self.stack[-1])
        return True
