import view.BaseClassEdit
from view.Widget import Widget

class BaseClassEdit(view.BaseClassEdit.BaseClassEdit, Widget):
    def __init__(self, path, subwidget_style):
        Widget.__init__(self, path+('value', ), subwidget_style)
        self.path = path
        self.positions = {}
        self.radii = {}
    def add_subwidget(self, key, widget):
        Widget.add_subwidget(self, key, widget)
        from functools import partial
        handler = partial(self.move_inner_cursor, key)
        widget.event_move_cursor.register(handler)
    def move_inner_cursor(self, key, direction):
        for row_index, row in enumerate(self.rows):
            if key in row:
                break
        else:
            assert False, 'didnt find widget'
        col_index = row.index(key)
        if direction in ['left', 'right']:
            delta = 1 if direction == 'right' else -1
            col_index += delta
            if 0 <= col_index < len(row):
                self.cursors['keyboard'].set(row[col_index])
                return
        else:
            delta = 1 if direction == 'down' else -1
            row_index += delta
            if 0 <= row_index < len(self.rows):
                self.cursors['keyboard'].set(self.rows[row_index][0])
                return
        self.event_move_cursor(direction)
    def calc_rows(self, (width, height)):
        ratio = width * 1. / height
        if ratio < 1:
            ratio = 1
        num_fields = len(self.subwidgets)
        import itertools
        num_places = last = 0
        for num_rows in itertools.count(1):
            row_size = num_rows / ratio
            last = num_places
            num_places = num_rows*row_size
            if num_places > num_fields:
                break
        if (last
            and num_fields-last <= num_places-num_fields):
            num_rows -= 1
        num_per_row = num_fields * 1. / num_rows
        subs_iter = iter(self.subwidgets)
        done = 0
        self.rows = []
        for row_index in range(num_rows):
            row = []
            self.rows.append(row)
            nextdone = done + num_per_row
            num_cur_row = int(round(nextdone)-round(done))
            done = nextdone
            if 0 == num_cur_row:
                continue
            for i in range(num_cur_row):
                row.append(subs_iter.next())
    def calc_positions(self, size):
        self.calc_rows(size)
        width, height = size
        if not self.rows:
            return
        ysize = height / len(self.rows)
        y = ysize / 2
        for row in self.rows:
            if not row:
                continue
            xsize = width / len(row)
            x = xsize / 2
            for key in row:
                self.positions[key] = (x, y)
                x += xsize
            y += ysize
        self.calc_radii(size)
    def calc_radii(self, (width, height)):
        for sub in self.subwidgets:
            from lib.math import distance
            pos = self.positions[sub]
            others_pos = [
                distance(pos, self.positions[other])/2.5
                for other in self.subwidgets
                if other is not sub]
            min_distance = min(others_pos+list(pos))
            x, y = self.positions[sub]
            r = min_distance
            self.radii[sub] = min([r, x, y, width-x, height-y])
    def _draw(self, surface, dest_size):
        self.sync_fields()
        self.calc_positions(dest_size)
        for key in self.subwidgets:
            (x, y), r = self.positions[key], self.radii[key]
            yield key, ((x-r, y-r), (r*2, r*2))
        self.drawmore(surface)
    def drawmore(self, surface):
        pass
