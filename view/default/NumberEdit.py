from model import compute
from view.InstanceEdit import InstanceEdit

class NumberEdit(InstanceEdit):
    def text(self):
        val = compute(self.path)
        if val is None:
            return 'need a\nnumber'
        return str(val)
    def getval(self):
        val = compute(self.path)
        if val is None:
            return 0
        return val
    def setval(self, val):
        last_field = self.path[-1]
        if last_field.is_const():
            last_field.value = val
    def handle_key__BACKSPACE(self, key_event):
        val = self.getval()
        newval = val//10
        if val < 0:
            newval += 1
        self.setval(newval)
    def handle_key__MINUS(self, key_event):
        self.setval(-self.getval())
    def handle_anykey(self, key_event):
        if super(NumberEdit, self).handle_anykey(key_event):
            return True
        key_name = key_event.str
        if not '0' <= key_name <= '9':
            return False
        key_val = int(key_name)
        val = self.getval()
        sign = 1 if val >= 0 else -1
        newval = sign * key_val + 10 * val
        self.setval(newval)
        return True
