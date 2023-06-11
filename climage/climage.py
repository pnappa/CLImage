from io import StringIO
import kdtree
import functools


# for storing pixels within the kdtree
class PixelMapping:
    def __init__(self, r, g, b, code):
        self.coords = (r, g, b)
        self.code = code

    def __len__(self):
        return len(self.coords)

    def __getitem__(self, i):
        return self.coords[i]


# get the best term colour
@functools.lru_cache(maxsize=256)
def _best(color_type, palette, source):
    # lazily only generate palettes if necessary
    if color_kdtrees[color_type][palette] is None:
        populate_kdtree(color_type, palette)

    tr = color_kdtrees[color_type][palette]
    return tr.search_nn(source)[0].data.code


class color_types:
    truecolor = 0
    color256 = 1
    color16 = 2
    color8 = 3


def populate_kdtree(color_type, palette):
    # TODO: add assert for color_type?
    if color_type == color_types.color8:
        colors = _get_system_colors(palette)[:8]
    elif color_type == color_types.color16:
        colors = _get_system_colors(palette)[:]
    elif color_type == color_types.color256:
        colors = _get_system_colors(palette)[:]
        # credit: https://github.com/dom111/image-to-ansi/
        # these colours can be found by running colortest-256
        for r1 in [0, 95, 135, 175, 215, 255]:
            for g1 in [0, 95, 135, 175, 215, 255]:
                for b1 in [0, 95, 135, 175, 215, 255]:
                    colors.append(
                        [
                            r1,
                            g1,
                            b1,
                            16
                            + int(
                                str(int(5 * r1 // 255))
                                + str(int(5 * g1 // 255))
                                + str(int(5 * b1 // 255)),
                                6,
                            ),
                        ]
                    )

        for s in [
            8,
            18,
            28,
            38,
            48,
            58,
            68,
            78,
            88,
            98,
            108,
            118,
            128,
            138,
            148,
            158,
            168,
            178,
            188,
            198,
            208,
            218,
            228,
            238,
        ]:
            colors.append([s, s, s, 232 + s // 10])

    color_kdtrees[color_type][palette] = kdtree.create(
        [PixelMapping(*col) for col in colors]
    )


palettes = [
    "default",
    "xterm",
    "linuxconsole",
    "solarized",
    "rxvt",
    "tango",
    "gruvbox",
    "gruvboxdark",
]
# store the generated kdtrees for palettes
color_kdtrees = {
    color_types.color256: {pal: None for pal in palettes},
    color_types.color16: {pal: None for pal in palettes},
    color_types.color8: {pal: None for pal in palettes},
}


def _get_system_colors(palette):
    # see extras/colorextract.py for details on getting these values
    if palette == "default":
        return [
            [0, 0, 0, 0],
            [128, 0, 0, 1],
            [0, 128, 0, 2],
            [128, 128, 0, 3],
            [0, 0, 128, 4],
            [128, 0, 128, 5],
            [0, 128, 128, 6],
            [192, 192, 192, 7],
            [128, 128, 128, 8],
            [255, 0, 0, 9],
            [0, 255, 0, 10],
            [255, 255, 0, 11],
            [0, 0, 255, 12],
            [255, 0, 255, 13],
            [0, 255, 255, 14],
            [255, 255, 255, 15],
        ]
    if palette == "xterm":
        return [
            [0, 0, 0, 0],
            [205, 0, 0, 1],
            [0, 205, 0, 2],
            [205, 205, 0, 3],
            [0, 0, 238, 4],
            [205, 0, 205, 5],
            [0, 205, 205, 6],
            [229, 229, 229, 7],
            [127, 127, 127, 8],
            [255, 0, 0, 9],
            [0, 255, 0, 10],
            [255, 255, 0, 11],
            [92, 92, 255, 12],
            [255, 0, 255, 13],
            [0, 255, 255, 14],
            [255, 255, 255, 15],
        ]
    elif palette == "linuxconsole":
        return [
            [0, 0, 0, 0],
            [170, 0, 0, 1],
            [0, 170, 0, 2],
            [170, 85, 0, 3],
            [0, 0, 170, 4],
            [170, 0, 170, 5],
            [0, 170, 170, 6],
            [170, 170, 170, 7],
            [85, 85, 85, 8],
            [255, 85, 85, 9],
            [85, 255, 85, 10],
            [255, 255, 85, 11],
            [85, 85, 255, 12],
            [255, 85, 255, 13],
            [85, 255, 255, 14],
            [255, 255, 255, 15],
        ]
    elif palette == "solarized":
        return [
            [7, 54, 66, 0],
            [220, 50, 47, 1],
            [133, 153, 0, 2],
            [181, 137, 0, 3],
            [38, 139, 210, 4],
            [211, 54, 130, 5],
            [42, 161, 152, 6],
            [238, 232, 213, 7],
            [0, 43, 54, 8],
            [203, 75, 22, 9],
            [88, 110, 117, 10],
            [101, 123, 131, 11],
            [131, 148, 150, 12],
            [108, 113, 196, 13],
            [147, 161, 161, 14],
            [253, 246, 227, 15],
        ]
    elif palette == "rxvt":
        return [
            [0, 0, 0, 0],
            [205, 0, 0, 1],
            [0, 205, 0, 2],
            [205, 205, 0, 3],
            [0, 0, 205, 4],
            [205, 0, 205, 5],
            [0, 205, 205, 6],
            [250, 235, 215, 7],
            [64, 64, 64, 8],
            [255, 0, 0, 9],
            [0, 255, 0, 10],
            [255, 255, 0, 11],
            [0, 0, 255, 12],
            [255, 0, 255, 13],
            [0, 255, 255, 14],
            [255, 255, 255, 15],
        ]
    elif palette == "tango":
        return [
            [0, 0, 0, 0],
            [204, 0, 0, 1],
            [78, 154, 6, 2],
            [196, 160, 0, 3],
            [52, 101, 164, 4],
            [117, 80, 123, 5],
            [6, 152, 154, 6],
            [211, 215, 207, 7],
            [85, 87, 83, 8],
            [239, 41, 41, 9],
            [138, 226, 52, 10],
            [252, 233, 79, 11],
            [114, 159, 207, 12],
            [173, 127, 168, 13],
            [52, 226, 226, 14],
            [238, 238, 236, 15],
        ]
    elif palette == "gruvbox":
        return [
            [251, 241, 199, 0],
            [204, 36, 29, 1],
            [152, 151, 26, 2],
            [215, 153, 33, 3],
            [69, 133, 136, 4],
            [177, 98, 134, 5],
            [104, 157, 106, 6],
            [124, 111, 100, 7],
            [146, 131, 116, 8],
            [157, 0, 6, 9],
            [121, 116, 14, 10],
            [181, 118, 20, 11],
            [7, 102, 120, 12],
            [143, 63, 113, 13],
            [66, 123, 88, 14],
            [60, 56, 54, 15],
        ]
    elif palette == "gruvboxdark":
        return [
            [40, 40, 40, 0],
            [204, 36, 29, 1],
            [152, 151, 26, 2],
            [215, 153, 33, 3],
            [69, 133, 136, 4],
            [177, 98, 134, 5],
            [104, 157, 106, 6],
            [168, 153, 132, 7],
            [146, 131, 116, 8],
            [251, 73, 52, 9],
            [184, 187, 38, 10],
            [250, 189, 47, 11],
            [131, 165, 152, 12],
            [211, 134, 155, 13],
            [142, 192, 124, 14],
            [235, 219, 178, 15],
        ]

    else:
        raise ValueError("invalid palette {}".format(palette))


# convert a 8 or 16bit id [0, 15] to the ansi number
def _id_to_codepoint(in_id, is_bg):
    if in_id >= 8:
        if is_bg:
            return "10" + str(in_id - 8)
        else:
            return "9" + str(in_id - 8)
    else:
        if is_bg:
            return "4" + str(in_id)
        else:
            return "3" + str(in_id)


def convert_pixel_color(pixel, ctype=color_types.color256, palette="default"):
    """
    Convert an RGB triple into the color used by the ANSI colour sequence,
    depending on the color mode.

    Arguments:
        pixel   -- (r,g,b) tuple representing the pixel. Each pixel is an 8 bit value, in the range [0, 255].

    Keyword Arguments:
        ctype   -- the color depth to use, default color_types.color256
        palette -- if not using the truecolor depth, adjust how pixels map to the desired colourspace to match the colourscheme better.
    """
    # The ANSI sequence for a truecolor color is simply the RGB colours.
    if ctype == color_types.truecolor:
        return pixel[:3]

    # Whereas the 8, 16, or 256 color value depends on the palette. We find the
    # closest visually similar color.
    return _best(ctype, palette, pixel)


def get_ansi_pixel(pixel, ctype=color_types.color256, palette="default"):
    """
    Convert a single RGB pixel into an ANSI escape sequence representing that pixel.

    Arguments:
        pixel   -- (r,g,b) tuple representing the pixel. Each pixel is an 8 bit value, in the range [0, 255].

    Keyword Arguments:
        ctype   -- the color depth to use, default color_types.color256
        palette -- if not using the truecolor depth, adjust how pixels map to the desired colourspace to match the colourscheme better.
    """
    # Convert a single pixel into the ANSI escape sequence.
    color = convert_pixel_color(
        pixel,
        ctype=ctype,
        palette=palette,
    )
    if ctype == color_types.truecolor:
        return "\x1b[48;2;{};{};{}m  ".format(*color)
    if ctype == color_types.color256:
        return "\x1b[48;5;{}m  ".format(color)
    return "\x1b[{}m  ".format(_id_to_codepoint(color, is_bg=True))


def get_reset_code():
    """
    Get the ANSI escape sequence to return color to normal.
    """
    return "\x1b[0m"


def get_dual_unicode_ansi_pixels(
    top_pixel, bottom_pixel, ctype=color_types.color256, palette="default"
):
    """
    Convert two RGB pixels into an ANSI escape sequence representing those pixel using unicode.

    Arguments:
        top_pixel   -- (r,g,b) tuple representing the top pixel. Each pixel is an 8 bit value, in the range [0, 255].
        bottom_pixel   -- (r,g,b) tuple representing the bottom pixel. Each pixel is an 8 bit value, in the range [0, 255].

    Keyword Arguments:
        ctype   -- the color depth to use, default color_types.color256
        palette -- if not using the truecolor depth, adjust how pixels map to the desired colourspace to match the colourscheme better.
    """
    color_top = convert_pixel_color(
        top_pixel,
        ctype=ctype,
        palette=palette,
    )
    color_bottom = convert_pixel_color(
        bottom_pixel,
        ctype=ctype,
        palette=palette,
    )

    if ctype == color_types.truecolor:
        return "\x1b[48;2;{};{};{}m\x1b[38;2;{};{};{}m▄".format(
            *color_top, *color_bottom
        )
    if ctype == color_types.color256:
        return "\x1b[48;5;{}m\x1b[38;5;{}m▄".format(color_top, color_bottom)

    bg_codepoint = _id_to_codepoint(color_top, is_bg=True)
    fg_codepoint = _id_to_codepoint(color_bottom, is_bg=False)
    return "\x1b[{}m\x1b[{}m▄".format(bg_codepoint, fg_codepoint)


def _toAnsi(img, oWidth, is_unicode, color_type, palette):
    destWidth = img.width
    destHeight = img.height
    scale = destWidth / oWidth
    destWidth = oWidth
    destHeight = int(destHeight // scale)

    # trim the height to an even number of pixels
    # (we draw two rows at a time in the unicode version)
    if is_unicode:
        destHeight -= destHeight % 2
    else:
        # for ascii, we need two columns to have square pixels (rows are twice the size
        # of  columns).
        destWidth //= 2
        destHeight //= 2

    # resize to new size
    img = img.resize((destWidth, destHeight))
    # where the converted string will be put in
    ansi_build = StringIO()

    yit = iter(range(destHeight))
    for y in yit:
        for x in range(destWidth):
            pix = img.getpixel((x, y))
            if is_unicode:
                # the next row's pixel
                bottom_pix = img.getpixel((x, y + 1))
                ansi_build.write(
                    get_dual_unicode_ansi_pixels(
                        pix, bottom_pix, ctype=color_type, palette=palette
                    )
                )
            else:
                ansi_build.write(get_ansi_pixel(pix, ctype=color_type, palette=palette))
        # Line ending, reset colours
        # We do this not to affect the surrounding terminal content.
        ansi_build.write("{}\n".format(get_reset_code()))
        if is_unicode:
            # skip a row because we do two rows at once
            next(yit, None)

    return ansi_build.getvalue()
