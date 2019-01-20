#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import __version__
from .climage import _toAnsi
from .climage import _color_types

from PIL import Image
import argparse
import sys

def _get_color_type(is_truecolor, is_256color, is_16color, is_8color):
    assert int(bool(is_8color)) + int(bool(is_16color)) + int(bool(is_256color)) + int(bool(is_truecolor)) == 1 and "only pick one colormode"

    if is_truecolor:
        return _color_types.truecolor
    if is_256color:
        return _color_types.color256
    if is_16color:
        return _color_types.color16
    if is_8color:
        return _color_types.color8

def convert(filename, is_unicode=False, is_truecolor=False, is_256color=True, is_16color=False, is_8color=False, width=80, palette="xterm"):
    # open the img, but convert to rgb because this fails if grayscale 
    # (assumes pixels are at least triplets)
    im = Image.open(filename).convert('RGB')
    ctype = _get_color_type(is_truecolor=is_truecolor, is_256color=is_256color, is_16color=is_16color, is_8color=is_8color)
    return _toAnsi(im, oWidth=width, is_unicode=is_unicode, color_type=ctype, palette=palette)

def to_file(infile, outfile, is_unicode=False, is_truecolor=False, is_256color=True, is_16color=False, is_8color=False, width=80, palette="xterm"):
    with open(outfile, 'w') as ofile:
        ansi_str = convert(infile, is_unicode=is_unicode, is_truecolor=is_truecolor, is_256color=is_256color, is_16color=is_16color, is_8color=is_8color, width=width, palette=palette)
        ofile.write(ansi_str)

def main():
    arg_parser = argparse.ArgumentParser(
            prog='climage',
            description="An easy way to convert images for display in terminals",
            epilog='',
            add_help=True,
            )

    arg_parser.add_argument('-v', '--version', action='version',
                            version='climage {0}'.format(__version__))

    character_type_group = arg_parser.add_mutually_exclusive_group()
    character_type_group.add_argument('--unicode', '-u', help='Sets the output to utilise unicode characters, resulting in a more detailed image. Warning: this is not supported by all terminals.', action="store_true")
    character_type_group.add_argument('--ascii', '-a', help='Restricts the output to ascii characters (default).', action="store_true", default=True)

    color_type_group = arg_parser.add_mutually_exclusive_group()
    color_type_group.add_argument('--truecolor', '-t', help="Utilise 16 million colors to encode output, results in more accurate output. Warning: RGB color is not supported by all terminals.", action="store_true")
    color_type_group.add_argument('--256color', '-m', dest='color256', help="Only use 256 colors to encode output (default).", action="store_true")
    color_type_group.add_argument('--16color', '-s', dest='color16', help="Only use 16 colors to encode output.", action="store_true")
    color_type_group.add_argument('--8color', '-b', dest='color8', help="Only use 8 colors to encode output.", action="store_true")

    arg_parser.add_argument('--palette', '-p', choices=["xterm", "rxvt", "solarized", "tango", "linuxconsole"], default=None, help="Choose a system color palette - only applies to 16 or 256 color modes. This is especially helpful for terminal themes that drastically change the appearance of default collors, achieving more accurate colors on those terminals.")

    arg_parser.add_argument('--quiet', '-q', action="store_true", default=False, help="Disable warnings.")

    arg_parser.add_argument('-w', '--cols', default=80, metavar='cols', help='Set the number of columns output should contain (default 80).', type=int)

    arg_parser.add_argument('-o', '--output', metavar='outfile', dest='outfile', help="Choose a file to output to", default='-')

    arg_parser.add_argument('inputfile', help="The image file you wish to convert.")

    args = arg_parser.parse_args()
    infile = args.inputfile
    outfile = args.outfile

    # whether unicode characters can be used
    is_unicode = False
    if args.unicode:
        is_unicode = True

    # what mode of color should be used
    is_truecolor = args.truecolor
    is_256color = args.color256
    is_16color = args.color16
    is_8color = args.color8

    if not is_truecolor and not is_256color and not is_16color and not is_8color:
        is_256color = True

    # width of the output image
    num_cols = args.cols

    if args.palette and is_truecolor and not args.quiet:
        print('WARNING: Choosing palette with truecolor has no effect.', file=sys.stderr)
    palette = args.palette if args.palette else "xterm"

    # print to file, or stdout?
    if outfile != '-':
        to_file(infile, outfile, is_unicode=is_unicode, is_truecolor=is_truecolor, is_256color=is_256color, is_16color=is_16color, is_8color=is_8color, width=num_cols, palette=palette)
    else:
        print(convert(infile, is_unicode=is_unicode, is_truecolor=is_truecolor, is_256color=is_256color, is_16color=is_16color, is_8color=is_8color, width=num_cols, palette=palette))
