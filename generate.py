"""
Generate hackerspaces.org logo as SVG.

Dependencies: The svgwrite library. Install it using pip.

Author: Danilo Bargen <mail@dbrgn.ch>
License: CC0 / Public Domain

"""
import svgwrite
from svgwrite import shapes, container

_type = 'sq'           # [dt|sq] Desired type of drawing. Dot or Square.
gridy = 10             # Grid size
radius = 6.5           # Radius of a dot, or side of a square
height = 566           # Height of the entire logo
width = 800            # Width of the entire logo
spacing = 20           # Spacing between spaceship and text
filename = 'logo.svg'  # Filename of the logo

color_bg = svgwrite.rgb(27, 28, 32)
color_fg = 'white'

spaceship = [
    '        o        ',
    '        o        ',
    '        o        ',
    '        o        ',
    '       ooo       ',
    ' o     ooo     o ',
    ' o    ooooo    o ',
    ' o    ooooo    o ',
    ' o   o ooo o   o ',
    'ooo ooo o ooo ooo',
    'oooooooo oooooooo',
    'oooooooo oooooooo',
    'oooooo ooo oooooo',
    'ooo oo ooo oo ooo',
    'o o  ooooooo  o o',
    'ooo  ooooooo  ooo',
    ' o    o o o    o ',
    ' o    ooooo    o ',
    '        o        ',
    '        o        ',
    ' o             o ',
    '                 ',
    ' o      o      o ',
    '                 ',
    ' o      o      o ',
    '                 ',
    '        o        ',
]
text = [
    'o                 o                                                    ',
    'o                 o                                                    ',
    'oooo   ooo   ooo  o   o  ooo  o oo   ooo   ooo   ooo   ooo   ooo   ooo ',
    'o   o     o o   o o  o  o   o  o  o o     o   o     o o   o o   o o    ',
    'o   o  oooo o     ooo   ooooo  o     ooo  o   o  oooo o     ooooo  ooo ',
    'o   o o   o o   o o  o  o      o        o o   o o   o o   o o         o',
    'o   o  oooo  ooo  o   o  ooo  ooo    ooo  oooo   oooo  ooo   ooo   ooo ',
    '                                          o                            ',
    '                                          o                            ',
]


def get_background():
    """
    Create background.
    """
    return dwg.rect((0, 0), (width, height), fill=color_bg)

def get_dot_group(pixels):
    """
    Given a list of lines, create an SVG group with dots on the grid.
    """
    # Create group
    group = container.Group()

    # Add dots
    for y, line in enumerate(pixels, start=1):
        for x, dot in enumerate(line, start=1):
            if dot == 'o':
                args = {
                    'center': (x * gridy, y * gridy),
                    'r': radius,
                    'stroke': color_fg,
                    'fill': color_fg,
                }
                circle = shapes.Circle(**args)
                group.add(circle)
    return group


def get_sq_group(pixels):
    """
    Given a list of lines, create an SVG group with dots on the grid.
    """
    # Create group
    group = container.Group()

    # Add dots
    for y, line in enumerate(pixels, start=1):
        for x, dot in enumerate(line, start=1):
            if dot == 'o':
                args = {
                    'insert':   (x*gridy, y*gridy), 
                    'size':     (radius, radius),
                    'fill':     color_fg, 
                    'stroke':   color_fg
                }
                rect = dwg.rect(**args)
                group.add(rect)    
    return group

def get_spaceship():
    """
    Create SVG group with spaceship.
    """
    # Get dots
    if _type == 'sq': group = get_sq_group(spaceship)
    if _type == 'dt': group = get_dot_group(spaceship)
    # Translate group to center
    spaceship_width = len(spaceship[0]) * gridy
    group.translate((width / 2) - (spaceship_width / 2))

    return group


def get_text():
    """
    Create SVG group with text.
    """
    # Get dots
    if _type == 'sq': group = get_sq_group(text)
    if _type == 'dt': group = get_dot_group(text)

    # Translate group to center
    text_width = len(text[0]) * gridy
    spaceship_height = len(spaceship) * gridy
    group.translate((width / 2) - (text_width / 2), spaceship_height + spacing)

    return group


if __name__ == '__main__':
    dwg = svgwrite.Drawing(filename, profile='tiny')

    # Add background
    dwg.add(get_background())

    # Create group for all content
    group = container.Group()

    # Add content to group
    group.add(get_spaceship())
    group.add(get_text())

    # Translate group
    content_height = len(spaceship) * gridy+ spacing + len(text) * gridy
    group.translate(0, height / 2 - content_height / 2)

    # Add group to drawing
    dwg.add(group)

    # Save SVG
    dwg.save()
    print('Done, saved to %s' % filename)
