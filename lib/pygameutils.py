import pygame

# The K_XXX constants of pygame are the pythonic names for keys.
# pygame.key.name does not generate pythonic names.
# For example: K_MINUS <=> "-"
key_names = dict((val, name[2:])
                for (name, val) in vars(pygame.constants).items()
                if name.startswith('K_'))

def draw_centered_text(surface, text, color):
    width, height = surface.get_size()
    x, y = width/2, height/2
    lines = [line.strip() for line in [_f for _f in text.splitlines() if _f]]
    from lib.font import find_font
    does_fit, font = find_font(lines, (width, height))
    if not does_fit:
        return
    pixels = [font.render(line, True, color) for line in lines]
    total_y = sum(p.get_size()[1] for p in pixels)
    cur_y = y-total_y/2
    for p in pixels:
        sx, sy = p.get_size()
        surface.blit(p, (x-sx/2, cur_y))
        cur_y += sy

