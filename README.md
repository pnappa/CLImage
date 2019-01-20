# CLImage

An easy way to convert images to colorful encoded sequences for displaying in terminals.

*TODO: add example image here*

# TODO:
    - check requires in setup.py
    - fix argparse reading in climage/main.py
    - write docstrings
    - investigate speeding up & lowering space of the `_rgb_to_ansi` fn. there are some clever algorithms i can use
    - might want to investigate accuracy of the existing color lookup

# Features
 - Custom sized images
 - ASCII or Unicode support
    - Unicode enables more detailed images
 - 256 color or Truecolor (16 million colors) support

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


