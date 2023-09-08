#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from . import __version__
from .climage import (
    _toAnsi,
    _best,
    palettes,
    color_types,
    get_dual_unicode_ansi_pixels,
    get_reset_code,
    get_ansi_pixel,
    convert_pixel_color,
)

from PIL import Image
import argparse
import sys
from io import StringIO


def _get_color_type(is_truecolor, is_256color, is_16color, is_8color):
    """Return an enum depending on which color is toggled. Exactly one must be toggled"""
    assert (
        int(bool(is_8color))
        + int(bool(is_16color))
        + int(bool(is_256color))
        + int(bool(is_truecolor))
        == 1
        and "only pick one colormode"
    )

    if is_truecolor:
        return color_types.truecolor
    if is_256color:
        return color_types.color256
    if is_16color:
        return color_types.color16
    if is_8color:
        return color_types.color8


def color_to_flags(color_type):
    """
    Convert a value of the color_types enum to kwargs accepted by the conversion functions.
    """
    ret = {
        "is_truecolor": color_type == color_types.truecolor,
        "is_256color": color_type == color_types.color256,
        "is_16color": color_type == color_types.color16,
        "is_8color": color_type == color_types.color8,
    }
    assert any(ret.values()), "Invalid color type supplied"
    return ret


def convert_pil(
    img,
    is_unicode=False,
    is_truecolor=False,
    is_256color=True,
    is_16color=False,
    is_8color=False,
    width=80,
    palette="default",
):
    """
    Convert an image, and return the resulting string.

    Arguments:
    img          -- A Pillow object representing the image to convert. Must be in RGB or RGBA format.

    Keyword Arguments:
    is_unicode      -- whether to use unicode in generating output (default False, ASCII will be used)
    is_truecolor    -- whether to use RGB colors in generation (few terminals support this). Exactly one color option must only be selected. Default False.
    is_256color     -- whether to use 256 colors (16 system colors, 6x6x6 color cube, and 24 grayscale colors) for generating the output. This is the default color setting. Please run colortest-256 for a demonstration of colors. Default True.
    is_16color      -- Whether to use only the 16 System colors. Default False
    is_8color       -- Whether to use only the first 8 of the System colors. Default False.
    width           -- Number of columns the output will use
    palette         -- Determines which RGB colors the System colors map to. This only is relevant when using 8/16/256 color modes. This may be one of ["default", "xterm", "linuxconsole", "solarized", "rxvt", "tango", "gruvbox", "gruvboxdark"]

    """
    ctype = _get_color_type(
        is_truecolor=is_truecolor,
        is_256color=is_256color,
        is_16color=is_16color,
        is_8color=is_8color,
    )
    return _toAnsi(
        img, oWidth=width, is_unicode=is_unicode, color_type=ctype, palette=palette
    )


def convert(
    filename,
    is_unicode=False,
    is_truecolor=False,
    is_256color=True,
    is_16color=False,
    is_8color=False,
    width=80,
    palette="default",
):
    """
    Convert an image, and return the resulting string.

    Arguments:
    infile          -- The name of the input file to load. Example: '/home/user/image.png'

    Keyword Arguments:
    is_unicode      -- whether to use unicode in generating output (default False, ASCII will be used)
    is_truecolor    -- whether to use RGB colors in generation (few terminals support this). Exactly one color option must only be selected. Default False.
    is_256color     -- whether to use 256 colors (16 system colors, 6x6x6 color cube, and 24 grayscale colors) for generating the output. This is the default color setting. Please run colortest-256 for a demonstration of colors. Default True.
    is_16color      -- Whether to use only the 16 System colors. Default False
    is_8color       -- Whether to use only the first 8 of the System colors. Default False.
    width           -- Number of columns the output will use
    palette         -- Determines which RGB colors the System colors map to. This only is relevant when using 8/16/256 color modes. This may be one of ["default", "xterm", "linuxconsole", "solarized", "rxvt", "tango", "gruvbox", "gruvboxdark"]

    """
    # open the img, but convert to rgb because this fails if grayscale
    # (assumes pixels are at least triplets)
    im = Image.open(filename).convert("RGB")
    return convert_pil(
        im,
        is_truecolor=is_truecolor,
        is_256color=is_256color,
        is_16color=is_16color,
        is_8color=is_8color,
        width=width,
        is_unicode=is_unicode,
        palette=palette,
    )


def convert_array(
    arr,
    is_unicode=False,
    is_truecolor=False,
    is_256color=True,
    is_16color=False,
    is_8color=False,
    palette="default",
):
    """
    Convert an array representing an image, and return the resulting string. Expects a numpy array or multi-dimensional representing an image in row-major format, with elements representing RGB triplets.

    Arguments:
    array          -- An list or numpy array whose elements represent an image. This must be in row-major format, in that array[0][0] represents the top left pixel, array[len(array)-1][0] represents the bottom left pixel, array[0][len(array[0])-1] represents the top right pixel, etc. The element at the root index must contain at least a 3 long vector, with the vector representing red, green, and blue components respectively. Each color must be in the range [0, 255] inclusive.

    Keyword Arguments:
    is_unicode      -- whether to use unicode in generating output (default False, ASCII will be used). If unicode is enabled, the input must be an even number of rows high.
    is_truecolor    -- whether to use RGB colors in generation (few terminals support this). Exactly one color option must only be selected. Default False.
    is_256color     -- whether to use 256 colors (16 system colors, 6x6x6 color cube, and 24 grayscale colors) for generating the output. This is the default color setting. Please run colortest-256 for a demonstration of colors. Default True.
    is_16color      -- Whether to use only the 16 System colors. Default False
    is_8color       -- Whether to use only the first 8 of the System colors. Default False.
    palette         -- Determines which RGB colors the System colors map to. This only is relevant when using 8/16/256 color modes. This may be one of ["default", "xterm", "linuxconsole", "solarized", "rxvt", "tango", "gruvbox", "gruvboxdark"]

    """
    ctype = _get_color_type(
        is_truecolor=is_truecolor,
        is_256color=is_256color,
        is_16color=is_16color,
        is_8color=is_8color,
    )

    assert (not is_unicode) or len(
        arr
    ) % 2 == 0, "Expecting even number of rows in array for unicode conversion"

    # where the converted string will be put in
    ansi_build = StringIO()

    yit = iter(range(len(arr)))
    for y in yit:
        for col in range(len(arr[y])):
            # Must be hashable for our kd-tree...
            pix = tuple(arr[y][col])
            assert len(pix) >= 3, "Expecting RGB or RGBA array"
            if is_unicode:
                bottom_pix = tuple(arr[y + 1][col])
                ansi_build.write(
                    get_dual_unicode_ansi_pixels(
                        pix, bottom_pix, ctype=ctype, palette=palette
                    )
                )
            else:
                ansi_build.write(get_ansi_pixel(pix, ctype=ctype, palette=palette))
        # Line ending, reset colours
        # We do this not to affect the surrounding terminal content.
        ansi_build.write("{}\n".format(get_reset_code()))
        if is_unicode:
            # skip a row because we do two rows at once
            next(yit, None)

    return ansi_build.getvalue()


def to_file(
    infile,
    outfile,
    is_unicode=False,
    is_truecolor=False,
    is_256color=True,
    is_16color=False,
    is_8color=False,
    width=80,
    palette="default",
):
    """
    Convert an image, and output to file.

    Arguments:
    infile          -- The name of the input file to load. Example: '/home/user/image.png'
    outfile         -- The name of the output file that the string will be written into.

    Keyword Arguments:
    is_unicode      -- Whether to use unicode in generating output (default False, ASCII will be used)
    is_truecolor    -- Whether to use RGB colors in generation (few terminals support this). Exactly one color option must only be selected. Default False.
    is_256color     -- Whether to use 256 colors (16 system colors, 6x6x6 color cube, and 24 grayscale colors) for generating the output. This is the default color setting. Please run colortest-256 for a demonstration of colors. Default True.
    is_16color      -- Whether to use only the 16 System colors. Default False
    is_8color       -- Whether to use only the first 8 of the System colors. Default False.
    width           -- Number of columns the output will use
    palette         -- Determines which RGB colors the System colors map to. This only is relevant when using 8/16/256 color modes. This may be one of ["default", "xterm", "linuxconsole", "solarized", "rxvt", "tango", "gruvbox", "gruvboxdark"]

    """
    with open(outfile, "w") as ofile:
        ansi_str = convert(
            infile,
            is_unicode=is_unicode,
            is_truecolor=is_truecolor,
            is_256color=is_256color,
            is_16color=is_16color,
            is_8color=is_8color,
            width=width,
            palette=palette,
        )
        ofile.write(ansi_str)


def main():
    arg_parser = argparse.ArgumentParser(
        prog="climage {0}".format(__version__),
        description="An easy way to convert images for display in terminals",
        epilog="",
        add_help=True,
    )

    arg_parser.add_argument(
        "-v", "--version", action="version", version="climage {0}".format(__version__)
    )

    character_type_group = arg_parser.add_mutually_exclusive_group()
    character_type_group.add_argument(
        "--unicode",
        "-u",
        help="Sets the output to utilise unicode characters, resulting in a more detailed image. Warning: this is not supported by all terminals.",
        action="store_true",
    )
    character_type_group.add_argument(
        "--ascii",
        "-a",
        help="Restricts the output to ascii characters (default).",
        action="store_true",
        default=True,
    )

    color_type_group = arg_parser.add_mutually_exclusive_group()
    color_type_group.add_argument(
        "--truecolor",
        "-t",
        help="Utilize 16 million colors to encode output, results in more accurate output. Warning: RGB color is not supported by all terminals.",
        action="store_true",
    )
    color_type_group.add_argument(
        "--256color",
        "-m",
        dest="color256",
        help="Only use 256 colors to encode output (default).",
        action="store_true",
    )
    color_type_group.add_argument(
        "--16color",
        "-s",
        dest="color16",
        help="Only use 16 colors to encode output.",
        action="store_true",
    )
    color_type_group.add_argument(
        "--8color",
        "-b",
        dest="color8",
        help="Only use 8 colors to encode output.",
        action="store_true",
    )

    arg_parser.add_argument(
        "--palette",
        "-p",
        choices=palettes,
        default=None,
        help="Choose a system color palette - only applies to 8, 16, or 256 color modes. This is especially helpful for terminal themes that drastically change the appearance of default collors, achieving more accurate colors on those terminals.",
    )

    arg_parser.add_argument(
        "--quiet", "-q", action="store_true", default=False, help="Disable warnings."
    )

    arg_parser.add_argument(
        "-w",
        "--cols",
        default=80,
        metavar="cols",
        help="Set the number of columns output should contain (default 80).",
        type=int,
    )

    arg_parser.add_argument(
        "-o",
        "--output",
        metavar="outfile",
        dest="outfile",
        help="Choose a file to output to",
        default="-",
    )

    arg_parser.add_argument("inputfile", help="The image file you wish to convert.")

    args = arg_parser.parse_args()
    infile = args.inputfile
    outfile = args.outfile

    # whether unicode characters can be used (default no. not all terminals support this)
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
        print(
            "WARNING: Choosing palette with truecolor has no effect.", file=sys.stderr
        )
    palette = args.palette if args.palette else "default"

    # print to file, or stdout?
    if outfile != "-":
        to_file(
            infile,
            outfile,
            is_unicode=is_unicode,
            is_truecolor=is_truecolor,
            is_256color=is_256color,
            is_16color=is_16color,
            is_8color=is_8color,
            width=num_cols,
            palette=palette,
        )
    else:
        print(
            convert(
                infile,
                is_unicode=is_unicode,
                is_truecolor=is_truecolor,
                is_256color=is_256color,
                is_16color=is_16color,
                is_8color=is_8color,
                width=num_cols,
                palette=palette,
            )
        )
