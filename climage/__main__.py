#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import __version__
from .climage import _toAnsi

from PIL import Image
import argparse

def convert(filename, is_unicode=False, is_truecolor=False, width=80):
    # open the img, but convert to rgb because this fails if grayscale 
    # (assumes pixels are at least triplets)
    im = Image.open(filename).convert('RGB')
    return _toAnsi(im, oWidth=width, is_unicode=is_unicode, is_truecolor=is_truecolor)

def to_file(infile, outfile, is_unicode=False, is_truecolor=False, width=80):
    with open(outfile, 'w') as ofile:
        ansi_str = convert(infile, is_unicode=is_unicode, is_truecolor=is_truecolor, width=width)
        ofile.write(convert)

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
    color_type_group.add_argument('--256', '-m', help="Only use 256 colors to encode output (default).", action="store_true", default=True)

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
    is_truecolor = False
    if args.truecolor:
        is_truecolor = True

    # width of the output image
    num_cols = args.cols

    # print to file, or stdout?
    if outfile != '-':
        to_file(infile, outfile, is_unicode=is_unicode, is_truecolor=is_truecolor, width=num_cols)
    else:
        print(convert(infile, is_unicode=is_unicode, is_truecolor=is_truecolor, width=num_cols))


# TODO: remove this
if __name__ == "__main__":
    main()

