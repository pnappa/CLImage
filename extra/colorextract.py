
"""
Dumps RGB->ANSI color mappings for given palettes.
Output colors are in the form [[r,g,b, ansinum], ...]

To generate these palettes, take a screenshot of the section called "System colors"
when running colortest-256. Ensure that the screenshot is the same orientation as
is presented (black should be top left, white should be bottom right), and that no
additional colors are present except for the 16.

The images in this folder are screenshots of the output of colortest after
selecting different color profiles in gnome-terminal.
"""

from PIL import Image

profiles = {"linuxconsole": "linuxconsole.png", "rxvt": "rxvt.png", "solarized": "solarized.png", "tango": "tango.png", "xterm": "xterm.png"}

for profilename, filename in profiles.items():
    colors = []
    im = Image.open(filename)
    # scan through the image, 
    # colors are assigned left to right, top to bottom 
    # first color is 0
    c_ansi = 0
    seen_colors = set()
    for col in im.getdata():
        if col in seen_colors:
            continue

        seen_colors.add(col)
        colors.append([*col, c_ansi])
        c_ansi += 1

    # if it fails here, it means you didn't crop the image properly
    # or, the palette re-uses colors... uh, you'll have to create your own tool for that
    assert len(seen_colors) == 16
    print(profilename)
    print(colors)

