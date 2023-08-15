class Style(object):
    def __init__(self, widget_for_funcs):
        self.widget_for_funcs = widget_for_funcs
    def __call__(self, obj):
        for func in self.widget_for_funcs:
            widget = func(obj, self)
            if widget is not None:
                return widget
        return None
    def copy(self):
        import copy
        res = copy.copy(self)
        return res
