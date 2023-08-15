import weakref
from lib.pygameutils import key_names
from lib import events
from functools import partial

import pygame

_mousebuttonname = {
    1 : 'left',
    2 : 'middle',
    3 : 'right',
    4 : 'scrollup',
    5 : 'scrolldown',
}

class Cursor(object):
    def __init__(self, name, widget):
        self.name = name
        self._widget = weakref.ref(widget)
        self.active = False
        self.key = None
        self.event_deactivated = events.Event()
        self.event_activated = events.Event()
    def subwidget(self):
        return self._widget().subwidgets.get(self.key)
    def subcursor(self):
        widget = self.subwidget()
        if widget is None:
            return None
        return widget.cursors[self.name]
    def activate(self):
        if self.active:
            return
        self.active = True
        cursor = self.subcursor()
        if cursor is not None:
            cursor.activate()
        else:
            self.event_activated()
    def deactivate(self):
        if not self.active:
            return
        self.active = False
        cursor = self.subcursor()
        if cursor is not None:
            cursor.deactivate()
        else:
            self.event_deactivated()
    def final_subwidget(self):
        cursor = self.subcursor()
        if cursor is None:
            return self._widget()
        return cursor.final_subwidget()
    def copy(self, src_cursor):
        self.set(src_cursor.key)
        cursor = self.subcursor()
        if cursor is not None:
            cursor.copy(src_cursor.subcursor())
    def set(self, key):
        if key == self.key:
            return
        prev_cursor = self.subcursor()
        if prev_cursor is not None:
            prev_cursor.deactivate()
        self.key = key
        new_cursor = self.subcursor()
        if new_cursor is not None:
            new_cursor.activate()

        if prev_cursor is None and new_cursor is not None:
            # Cursor becomes non-None
            self.event_deactivated()
        elif prev_cursor is not None and new_cursor is None:
            # Cursor becomes None
            self.event_activated()

class Widget(object):
    outline_color_of_state = [
        ('draw_outline', (4, (150, 150, 150))),

        # TODO: Hack: These should be moved to the various subclasses:
        ('link_src', (4, (255, 255, 255))),
        ('drag_src', (4, (255, 100, 100))),
        
        ('active_cursor_keyboard', (4, (100, 100, 255))),
        ('active_cursor_mouse', (2, (180, 180, 150))),

    ]
    draw_outline = False
    pass_cursors_to_single_child = True
    def __init__(self, key, subwidget_style):
        self.key = key
        self.subwidget_style = subwidget_style
        self.subwidgets = {}
        self.event_move_cursor = events.Event()
        self.event_move_out = events.Event()
        self.cursors = {'keyboard' : Cursor('keyboard', self),
                        'mouse' : Cursor('mouse', self)}
        for name, cursor in self.cursors.items():
            for event_name in ['activated', 'deactivated']:
                event = getattr(cursor, 'event_%s' % (event_name,))
                handler = getattr(self, 'cursor_%s' % (event_name,))
                event.register(partial(handler, name))
        self.prev_keyboard_cursor = None
        self._states = set()
        self.anim_rects = {}
    def cursor_deactivated(self, name):
        self.remove_state('active_cursor_%s' % (name,))
    def should_move_to_inner(self):
        # If our cursor was activated, we activate unambiguous children immediately.
        return (self.pass_cursors_to_single_child
            and len(self.subwidgets) == 1)
    def cursor_activated(self, name):
        self.add_state('active_cursor_%s' % (name,))
        if self.should_move_to_inner():
            key, = list(self.subwidgets.keys())
            self.cursors[name].set(key)
    def states(self):
        states = list(self._states)
        # TODO: Hack, remove this?
        if self.draw_outline:
            states.append('draw_outline')
        return states
    def add_state(self, state):
        self._states.add(state)
    def remove_state(self, state):
        self._states.discard(state)
    def add_subwidget(self, key, widget):
        self.subwidgets[key] = widget
        widget.event_move_out.register(self.handle_inner_moved_out)
    def handle_inner_moved_out(self):
        self.prev_keyboard_cursor = self.cursors['keyboard'].key
        self.cursors['keyboard'].set(None)
        if self.should_move_to_inner():
            self.event_move_out()
    def remove_subwidget(self, key):
        del self.subwidgets[key]
    def eventmeth_try(self, meth_prefix, eventname, *args):
        meth_name = '__'.join((meth_prefix, eventname))
        meth = getattr(self, meth_name, None)
        if meth is None:
            return False
        ret = meth(*args)
        if False == ret:
            return False
        return True
    def _keyname(self, key_event):
        return key_names.get(key_event.key, 'unknown').upper()
    def prehandle_anykey(self, key_event):
        return self.eventmeth_try('prehandle_key', self._keyname(key_event), key_event)
    def handle_anykey(self, key_event):
        return self.eventmeth_try('handle_key', self._keyname(key_event), key_event)
    def handle_keydown(self, key_event):
        if self.prehandle_anykey(key_event):
            return True
        cursor = self.cursors['keyboard']
        cursorwidget = cursor.subwidget()
        if (cursorwidget is not None
            and cursorwidget.handle_keydown(key_event)):
            return True
        if self.handle_anykey(key_event):
            return True
        return False
    def childrenpos_of_pos(self, pos):
        for key, rect in self.anim_rects.items():
            if (rect is not None and rect.collidepoint(pos)):
                rel_pos = tuple(p-tl for p,tl in zip(pos, rect.topleft))
                yield key, rel_pos
    def _update_mouse_cursor(self, pos):
        cursor = self.cursors['mouse']
        for key, rel_pos in self.childrenpos_of_pos(pos):
            cursor.set(key)
            # Only handle the first ambiguously pointed child:
            break
    def handle_mouse_event(self, pos, event):
        if event.type == pygame.MOUSEMOTION:
            self._update_mouse_cursor(pos)
        if self._handle_any_mouse_event('prehandle_mouse', event):
            return True
        # TODO: To send the event to the mouse cursor, rather than the
        # position? In which case, how to handle the rects?
        for key, rel_pos in self.childrenpos_of_pos(pos):
            if key not in self.subwidgets:
                continue
            if self.subwidgets[key].handle_mouse_event(rel_pos, event):
                return True
        if self._handle_any_mouse_event('handle_mouse', event):
            return True
        return False
    def _mousebuttonname(self, button_index):
        return _mousebuttonname.get(button_index, 'unknown')
    def _mouseeventname(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self._mousebuttonname(event.button) + '_down'
        elif event.type == pygame.MOUSEBUTTONUP:
            return self._mousebuttonname(event.button) + '_up'
        elif event.type == pygame.MOUSEMOTION:
            return 'motion'
    def _handle_any_mouse_event(self, prefix, event):
        return self.eventmeth_try(prefix, self._mouseeventname(event), event)

    draw_outline_only_if_only_frame = False
    fixed_frame_size = 6
    def draw_frame(self, surface):
        outline_color = None
        fw = 0
        cur_rect = surface.get_rect()
        if 'mark' in self.states():
            surface.fill((255, 255, 100))
        for state, (outline_width, outline_color) in self.outline_color_of_state:
            if state not in self.states():
                continue
            if (self.draw_outline_only_if_only_frame
                and state == 'draw_outline'
                and len(self.states()) > 1):
                continue
            double_width = (-outline_width*2,
                            -outline_width*2)
            cur_rect.inflate_ip(double_width)
            pygame.draw.rect(surface, outline_color, cur_rect, outline_width)
            fw += outline_width
        if self.fixed_frame_size is not None:
            return self.fixed_frame_size
        return fw
    def draw(self, surface, xxx_todo_changeme):
        (w, h) = xxx_todo_changeme
        fw = self.draw_frame(surface)
        subsurf = surface.subsurface(
            surface.get_rect().inflate(-fw*2, -fw*2))
        subdraws = self._draw(subsurf, (w-fw*2, h-fw*2))
        if subdraws is None:
            return
        from lib.iterfeeder import iterfeeder
        for setsend, (key, tr) in iterfeeder(subdraws):
            r = pygame.Rect(tr).move(fw, fw)
            send = yield key, r
            self.anim_rects[key] = send
            setsend(send)
    def handle_key__UP(self, key_event):
        self.event_move_cursor('up')
    def handle_key__DOWN(self, key_event):
        self.event_move_cursor('down')
    def handle_key__LEFT(self, key_event):
        self.event_move_cursor('left')
    def handle_key__RIGHT(self, key_event):
        self.event_move_cursor('right')
    def handle_key__ESCAPE(self, key_event):
        self.event_move_out()
    def handle_key__SPACE(self, key_event):
        if not self.subwidgets:
            return
        cursor = self.cursors['keyboard']
        cursor.set(next(iter(self.subwidgets.keys())))
