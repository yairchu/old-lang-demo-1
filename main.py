from view import mainloop
from model.field import ConstField, Field
from model import class_fields, metaclass
from nf_builtins import add, multiply, nfnumber
from model.pyapi import nf_setattr
import pickle
import sys

def make_world():
    Afield = ConstField({'label': 'A'}, nfnumber)
    Afield.value = 5
    Bfield = Field({'label': 'B'}, add)
    Cfield = Field({'label': 'C'}, nfnumber)
    worldfields = [
        Afield,
        Bfield,
        Cfield,
        ]
    worldlinks = {
        #(Cfield, ): (Afield, ),
        }
    
    worldclassfield = ConstField({'label': 'world class'}, metaclass)
    worldclass = (worldclassfield, )
    nf_setattr(worldclass, class_fields.fields, worldfields)
    nf_setattr(worldclass, class_fields.links, worldlinks)
    
    worldfield = ConstField({'label': 'root'}, worldclass)
    path = (worldfield,)
    return path

def main():
    import nf_builtins
    if sys.argv[1:] == ['-l']:
        state = pickle.load(open('state.pkl', 'rb'))
        world, cf, bt = state
        for key, value in cf.items():
            setattr(class_fields, key, value)
        for key, value in bt.items():
            setattr(nf_builtins, key, value)
    else:
        world = make_world()
    mainloop.mainloop(world)
    def for_pickle(thing):
        from types import ModuleType
        return dict((key, val)
                    for key, val in thing.__dict__.items()
                    if not key.startswith('_')
                    and not isinstance(val, ModuleType))
    state = world, for_pickle(class_fields), for_pickle(nf_builtins)
    pickle.dump(state, open('state.pkl', 'wb'))

try:
    main()
except:
    import pygame
    pygame.quit()
    import sys
    sys.last_type, sys.last_value, sys.last_traceback = sys.exc_info()
    import traceback
    print('-------- Exception:')
    print()
    for line in traceback.format_exception_only(sys.last_type, sys.last_value):
        print(line)
    import pdb
    pdb.pm()
    
