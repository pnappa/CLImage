# CLImage

An easy way to convert images to colorful encoded sequences for displaying in terminals.

*TODO: add example image here*

# TODO:
    - write docstrings
    - investigate speeding up & lowering space of the `_rgb_to_ansi` fn. there are some clever algorithms i can use
        - prebake a voronoi diagram into a trapezoidal map, which can be queried in logn time: https://stackoverflow.com/a/1901885/1129185
    - might want to investigate accuracy of the existing color lookup
        - looks good, esp with customisable palettes
    - investigate different scaling modes? 256 color sometimes looks better for colors (than truecolor)?
    - rename the `_toAnsi` fn, as it's not really right (ANSI is restricted to the 16 color stuff, right?)
    - investigate why solarized palette looks worse on solarized theme..?
    - add a detect option to --palette, to automatically detect mapping of system colors? this might be hard.

# Features
 - Custom sized images
 - ASCII or Unicode support
    - Unicode enables 4x more detail
 - 8/16/256/Truecolor support, for a wider gamut of colors
 - Selectable system palettes to adjust for user terminal themes

# Usage

CLImage is available as both a standalone CLI program, or available for import as a Python3 library.

## CLI Program

By default converting an image will output in 256 color, as 80 columns, and ASCII.
```bash
$ climage image.png
```
*TODO: add output image*

A nicer image can be obtained when enabling unicode and truecolor flags.
```bash
$ climage --unicode --truecolour image.png
```
*TODO: add output image*

Further options may be found by running `climage --help`

## Python Library

Detail:
    - some `to_file` fn? outputs the image to file
    - some simple `convert` fn, that returns a string of the image

```python3
import climage
```
*TODO: actually decide m8*


