import math
import subprocess
from PIL import Image
import sys
import os
import functools

import argparse

# python pseudo-port of https://github.com/dom111/image-to-ansi

colour_mapping = []

def _rgb_to_256(r, g, b):
    # TODO: i reckon I can replace this with a fast voronoi version
    # i.e. generate voronoi boundaries offline, then find which
    # bound the point is in.
    global colour_mapping
    def gen_colours():
        # credit: https://github.com/dom111/image-to-ansi/
        # I actually don't know how he came up with these colours
        colour_mapping.append([0, 0, 0, 0])
        colour_mapping.append([128, 0, 0, 1])
        colour_mapping.append([0, 128, 0, 2])
        colour_mapping.append([128, 128, 0, 3])
        colour_mapping.append([0, 0, 128, 4])
        colour_mapping.append([128, 0, 128, 5])
        colour_mapping.append([0, 128, 128, 6])
        colour_mapping.append([192, 192, 192, 7])
        colour_mapping.append([128, 128, 128, 8])
        colour_mapping.append([255, 0, 0, 9])
        colour_mapping.append([0, 255, 0, 10])
        colour_mapping.append([255, 255, 0, 11])
        colour_mapping.append([0, 0, 255, 12])
        colour_mapping.append([255, 0, 255, 13])
        colour_mapping.append([0, 255, 255, 14])
        colour_mapping.append([255, 255, 255, 15])

        for r1 in [0, 95, 135, 175, 215, 255]:
            for g1 in [0, 95, 135, 175, 215, 255]:
                for b1 in [0, 95, 135, 175, 215, 255]:
                    colour_mapping.append([r1,g1,b1, 16 + int(str(math.floor(5 * r1/255)) + 
                                                str(math.floor(5 * g1/255)) + 
                                                str(math.floor(5 * b1/255)),6)])

        for s in [8, 18, 28, 38, 48, 58, 68, 78, 88, 98, 108, 118, 128, 138, 148, 158, 168, 178, 188, 198, 208, 218, 228, 238]:
            colour_mapping.append([s, s, s, 232 + s//10])

    if len(colour_mapping) == 0:
        gen_colours()

    r,g,b = map(int, (r,g,b))

    # get the best term colour
    def best(candidates, source):
        # based on the distance from the populated colour table - closest wins!
        return min(candidates, key=lambda x: abs(x[0] - source[0]) + abs(x[1] - source[1]) + abs(x[2] - source[2]))

    return best(colour_mapping, [r,g,b])[3]


# convert the rgb value into an escape sequence
def _pix_to_escape(r, g, b, is_truecolor):
    if is_truecolor:
        return '\x1b[48;2;{};{};{}m  '.format(r,g,b)
    else:
        return '\x1b[48;5;{}m  '.format(_rgb_to_256(r,g,b))

# convert the two row's colors to a escape sequence (unicode does two rows at a time)
def _dual_pix_to_escape(r1, r2, g1, g2, b1, b2, is_truecolor):
    if is_truecolor:
        return '\x1b[48;2;{};{};{}m\x1b[38;2;{};{};{}m▄'.format(r1,g1,b1, r2,g2,b2)
    else
        return '\x1b[48;5;{}m\x1b[38;5;{}m▄'.format(_rgb_to_256(r1,g1,b1), _rgb_to_256(r2, g2, b2))

def _toAnsi(img, oWidth, is_unicode=False, is_truecolor=False):
    destWidth = img.width
    destHeight = img.height
    # produce a scale if the image is too big
    if destWidth > oWidth:
        scale = destWidth / oWidth
        destWidth = oWidth
        destHeight = math.floor(destHeight/scale)

    # trim the height to an even number of pixels 
    # (we draw two rows at a time in the unicode version)
    if is_unicode:
        destHeight -= destHeight % 2

    # resize to new size
    img = img.resize((destWidth, destHeight))
    # where the converted string will be put in
    ansi_string = ''

    yit = iter(range(destHeight))
    for y in yit:
        for x in range(destWidth):
            r,g,b = map(str, img.getpixel((x, y)))
            if is_unicode:
                # the next row's pixel
                rprime, gprime, bprime = map(str, img.getpixel((x, y+1)))
                ansi_string += _dual_pix_to_escape(r,rprime, g, gprime, b, bprime, is_truecolor)
            else:
                ansi_string += _pix_to_escape(r,g,b, is_truecolor)
        # line ending, reset colours
        ansi_string += '\x1B[0m\n'
        if is_unicode:
            # skip a row because we do two rows at once
            next(yit, None)

    return ansi_string

def convert(filename, is_unicode=False, is_truecolor=False, width=80):
    # open the img, but convert to rgb because this fails if grayscale 
    # (assumes pixels are at least triplets)
    im = Image.open(filename).convert('RGB')
    return _toAnsi(im, oWidth=width, is_unicode=is_unicode, is_truecolor=is_truecolor)

def to_file(infile, outfile, is_unicode=False, is_truecolor=False, width=80):
    with open(outfile, 'w') as ofile:
        ansi_str = convert(infile, is_unicode, is_truecolor, width)
        ofile.write(convert)

def main():
    working_dir = os.getcwd()
    # TODO: argparse.
    arg_parser = argparse.ArgumentParser(
            prog='climage',
            description="An easy way to convert images for display in terminals",
            add_help=True,
            allow_abbrev=True
            )

    arg_parser.add_argument('-o', '--output', metavar='outfile', dest='output_file', help="Choose a file to output to")
    # TODO: how do I read this value
    arg_parser.add_argument('--unicode', help='Sets the output to utilise unicode characters, resulting in a more detailed image. Warning: this is not supported by all terminals.')
    arg_parser.add_argument('--ascii', help='Restricts the output to ascii characters (default).')
    arg_parser.add_argument('-w', '--cols', default=80, metavar='cols', help='Set the number of columns output should contain (image is scaled to this value).')
    arg_parser.add_argument('-t', '--truecolor', help="Utilise 16 million colors to encode output, results in more accurate output. Warning: RGB color is not supported by all terminals.")
    arg_parser.add_argument('-m', '--256', help="Only use 256 colors to encode output (default).")

    args = arg_parser.parse_args(sys.argv)

    print(args)


# TODO: remove this
if __name__ == "__main__":
    #print(convert(sys.argv[1], is_256=True, is_unicode=True, width=80))
    main()

