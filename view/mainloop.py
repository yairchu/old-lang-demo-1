# TODO:
# - split to files
# - have generic handle_key

import pygame

def iter_events():
    return pygame.event.get()

def _mainloop(path):
    resolution = (800, 600)
    screen = pygame.display.set_mode(resolution)
    from . import styles
    from .Browser import Browser
    from .Animator import Animator
    anim = Animator()
    browser = Browser(styles.literal)
    browser.enter(path)
    clock = pygame.time.Clock()
    quit_mods = pygame.KMOD_CTRL | pygame.KMOD_META
    while True:
        clock.tick(25)
        for event in iter_events():
            if pygame.KEYDOWN == event.type:
                if (pygame.K_q == event.key
                    and (quit_mods & event.mod)):
                    return
                browser.handle_keydown(event)
            elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
                browser.handle_mouse_event(event.pos, event)
            if pygame.QUIT == event.type:
                return
        fillcolor = (200, 200, 200)
        screen.fill(fillcolor)
        anim.draw(screen, browser)
        pygame.display.update()

def mainloop(menu_subinstance):
    pygame.init()
    try:
        _mainloop(menu_subinstance)
    finally:
        pygame.quit()
