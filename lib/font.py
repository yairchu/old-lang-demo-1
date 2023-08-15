import pygame

pygame.font.init()
fonts = list(
    pygame.font.SysFont(pygame.font.get_default_font(), int(i**1.1))
    for i in range(5, 100)
)

def approximate_binary_search(items, cmp):
    if not items:
        raise IndexError("Cannot find matching item")
    if len(items) == 1:
        return items[0]
    mid = len(items)//2
    item = items[mid]
    c = cmp(item)
    if c > 0:
        return approximate_binary_search(items[:mid], cmp)
    elif c < 0:
        return approximate_binary_search(items[mid:], cmp)
    else:
        return item

def find_font(lines, xxx_todo_changeme):
    (max_width, max_height) = xxx_todo_changeme
    def does_fit(font):
        if font.get_height() * len(lines) > max_height:
            return 1
        for line in lines:
            # There's a bug in pygame/SDL where if antialias=False,
            # SDL_ttf render fails for strings that contain spaces.
            width, height = font.size(line)
            if width > max_width:
                return 1
        return -1
    font = approximate_binary_search(fonts, does_fit)
    return does_fit(font) == -1, font
