from Widget import Widget

class WidgetList(Widget):
    class Horizontal(object):
        directions = dict(left = -1, right = 1)
        index = 0
    class Vertical(object):
        directions = dict(up = -1, down = 1)
        index = 1
    def __super(self):
        return super(WidgetList, self)
    def __init__(self, *args, **kwargs):
        self.__super().__init__(*args, **kwargs)
        self.subwidgets_order = []
        self.subwidgets_sizes = {}
    draw_outline = True    
    def add_subwidget(self, key, widget):
        self.__super().add_subwidget(key, widget)
        widget.event_move_cursor.register(self.move_inner_cursor)
        self.subwidgets_order.append(key)
    def remove_subwidget(self, key):
        self.__super().remove_subwidget(key)
        self.subwidgets_order.remove(key)
    def move_inner_cursor(self, direction):
        if direction not in self.dimension.directions:
            self.event_move_cursor(direction)
            return
        cursor = self.cursors['keyboard']
        if cursor.key is None:
            new_index = 0
        else:
            old_index = self.subwidgets_order.index(cursor.key)
            dir_index = self.dimension.directions[direction]
            new_index = old_index+dir_index
        if not 0 <= new_index < len(self.subwidgets_order):
            self.event_move_cursor(direction)
            return
        cursor.set(self.subwidgets_order[new_index])
    def _draw(self, surface, dest_size):
        fixed_count = len(self.subwidgets_sizes)
        fixed_sizes_sum = sum(self.subwidgets_sizes.itervalues())
        axis = self.dimension.index
        subsize = list(dest_size)
        total_count = len(self.subwidgets)
        var_count = total_count-fixed_count
        subsize[axis] -= fixed_sizes_sum
        if var_count:
            subsize[axis] /= var_count
        pos = [0, 0]
        for key in self.subwidgets_order:
            cursize = subsize[:]
            if key in self.subwidgets_sizes:
                cursize[axis] = self.subwidgets_sizes[key]
            yield key, (pos, cursize)
            pos[axis] += cursize[axis]
