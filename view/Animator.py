from lib.iterfeeder import iterfeeder
import pygame

def animate(factor, src, dst):
    if abs(dst-src) <= 1:
        return dst
    r = src*(1-factor)+dst*factor
    if abs(dst-r) <= 1:
        return dst
    if src == int(round(r)) or abs(dst-r) > abs(dst-src):
        if src < dst:
            return src+1
        else:
            return src-1
    return int(round(r))

def rect2sides(rect):
    x, y, w, h = rect
    return x, y, x+w, y+h
def sides2rect((left, top, right, bottom)):
    return pygame.Rect(left, top, right-left, bottom-top)

class Animator(object):
    def __init__(self):
        self.prev_rects = {}
        self.show = set()
        self.paths_stumbled = set()
    def stumble_path(self, path):
        if path not in self.paths_stumbled:
            #print path
            pass
        self.paths_stumbled.add(path)
    def draw(self, surface, widget):
        rect = surface.get_rect()
        self.anim_finished = True
        self.toshow = set()
        self._draw(surface, rect, widget)
        for x in self.prev_rects.keys():
            if x not in self.toshow:
                del self.prev_rects[x]
        self.show.intersection_update(self.toshow)
        if self.anim_finished:
            self.show = self.toshow
        for t in self.show.copy():
            for i in range(len(t)-1):
                sub = t[:i]
                self.show.add(sub)
                # TODO: this is temporary hack
                self.show.add(sub+('value',))
    def calc_prev_rect(self, path, rect):
        if path in self.prev_rects:
            return self.prev_rects[path]
        x, y, w, h = rect
        return pygame.Rect(x+w/2, y+h/2, 0, 0)
    def calc_anim_rect(self, path, rect):
        prev = rect2sides(self.calc_prev_rect(path, rect))
        sides = rect2sides(rect)
        rate = 0.2
        limit = 50
        from functools import partial
        anim = map(partial(animate, rate), prev, sides)
        animrect = sides2rect(anim)
        from operator import sub
        if max(map(abs, map(sub, anim, sides))) > limit:
            self.anim_finished = False
        self.prev_rects[path] = animrect
        return animrect
    def _draw(self, surface, rect, widget):
        path = widget.key
        self.stumble_path(path)
        assert path not in self.toshow, 'same key twice %r' % (path, )
        for i in range(len(path)+1):
            self.toshow.add(path[:i])
        if path not in self.show:
            return
        anim_rect = self.calc_anim_rect(path, rect)
        ax, ay, aw, ah = anim_rect
        clamped = anim_rect.clamp(surface.get_rect())
        subsurf = surface.subsurface(clamped)
        subdraws = widget.draw(subsurf, rect.size)
        if subdraws is None:
            # not a generator
            return
        for setsend, (key, relrecttup) in iterfeeder(subdraws):
            relrect = pygame.Rect(relrecttup)
            absrect = relrect.move(rect.topleft)
            subwidget = widget.subwidgets[key]
            subanim = self._draw(surface, absrect, subwidget)
            if subanim is None:
                setsend(None)
            else:
                setsend(subanim.move(-ax, -ay))
        return anim_rect
