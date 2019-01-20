""" CLImage entry point """

colour_mapping = []

# get the best term colour
def _best(candidates, source):
    # based on the distance from the populated colour table - closest wins!
    return min(candidates, key=lambda x: abs(x[0] - source[0]) + 
                                         abs(x[1] - source[1]) + 
                                         abs(x[2] - source[2]))

class _color_types:
    truecolor = 0
    color256 = 1
    color16 = 2
    color8 = 3

def _get_system_colors(palette):
    # see extras/colorextract.py for details on getting these values
    if palette == "xterm":
        return [[0, 0, 0, 0], [205, 0, 0, 1], [0, 205, 0, 2], [205, 205, 0, 3], [0, 0, 238, 4], [205, 0, 205, 5], [0, 205, 205, 6], [229, 229, 229, 7], [127, 127, 127, 8], [255, 0, 0, 9], [0, 255, 0, 10], [255, 255, 0, 11], [92, 92, 255, 12], [255, 0, 255, 13], [0, 255, 255, 14], [255, 255, 255, 15]]
    elif palette == "linuxconsole":
        return [[0, 0, 0, 0], [170, 0, 0, 1], [0, 170, 0, 2], [170, 85, 0, 3], [0, 0, 170, 4], [170, 0, 170, 5], [0, 170, 170, 6], [170, 170, 170, 7], [85, 85, 85, 8], [255, 85, 85, 9], [85, 255, 85, 10], [255, 255, 85, 11], [85, 85, 255, 12], [255, 85, 255, 13], [85, 255, 255, 14], [255, 255, 255, 15]]
    elif palette == "solarized":
        return [[7, 54, 66, 0], [220, 50, 47, 1], [133, 153, 0, 2], [181, 137, 0, 3], [38, 139, 210, 4], [211, 54, 130, 5], [42, 161, 152, 6], [238, 232, 213, 7], [0, 43, 54, 8], [203, 75, 22, 9], [88, 110, 117, 10], [101, 123, 131, 11], [131, 148, 150, 12], [108, 113, 196, 13], [147, 161, 161, 14], [253, 246, 227, 15]]
    elif palette == "rxvt":
        return [[0, 0, 0, 0], [205, 0, 0, 1], [0, 205, 0, 2], [205, 205, 0, 3], [0, 0, 205, 4], [205, 0, 205, 5], [0, 205, 205, 6], [250, 235, 215, 7], [64, 64, 64, 8], [255, 0, 0, 9], [0, 255, 0, 10], [255, 255, 0, 11], [0, 0, 255, 12], [255, 0, 255, 13], [0, 255, 255, 14], [255, 255, 255, 15]]
    elif palette == "tango":
        return [[0, 0, 0, 0], [204, 0, 0, 1], [78, 154, 6, 2], [196, 160, 0, 3], [52, 101, 164, 4], [117, 80, 123, 5], [6, 152, 154, 6], [211, 215, 207, 7], [85, 87, 83, 8], [239, 41, 41, 9], [138, 226, 52, 10], [252, 233, 79, 11], [114, 159, 207, 12], [173, 127, 168, 13], [52, 226, 226, 14], [238, 238, 236, 15]]
    else:
        raise ValueError("invalid palette {}".format(palette))

def _rgb_to_256(r, g, b, palette):
    # TODO: i reckon I can replace this with a fast voronoi version
    # i.e. generate voronoi boundaries offline, then find which
    # bound the point is in.
    # TODO: as it is, this is rather slow actually!
    def gen_colours():
        # credit: https://github.com/dom111/image-to-ansi/
        # I actually don't know how he came up with these colours
        for r1 in [0, 95, 135, 175, 215, 255]:
            for g1 in [0, 95, 135, 175, 215, 255]:
                for b1 in [0, 95, 135, 175, 215, 255]:
                    colour_mapping.append([r1, g1, b1, 16 + int(
                                                str(int(5 * r1 // 255)) + 
                                                str(int(5 * g1 // 255)) +
                                                str(int(5 * b1 // 255)), 6)])

        for s in [8, 18, 28, 38, 48, 58, 68, 78, 88, 98, 108, 118, 128, 138, 148, 158, 168, 178, 188, 198, 208, 218, 228, 238]:
            colour_mapping.append([s, s, s, 232 + s // 10])

    if len(colour_mapping) == 0:
        gen_colours()

    r, g, b = map(int, (r, g, b))

    return _best(colour_mapping + _get_system_colors(palette), [r, g, b])[3]

# convert a rgb color to the closest 16 color number
def _rgb_to_16(r, g, b, palette):
    r, g, b = map(int, (r, g, b))

    return _best(_get_system_colors(palette), [r, g, b])[3]

def _rgb_to_8(r, g, b, palette):
    # 8 bit is simply the non-dark versions of the 16 system colors
    r, g, b = map(int, (r, g, b))
    return _best(_get_system_colors(palette)[:8], [r, g, b])[3]

# convert the rgb value into an escape sequence
def _pix_to_escape(r, g, b, color_type, palette):
    if color_type == _color_types.truecolor:
        return '\x1b[48;2;{};{};{}m  '.format(r, g, b)
    elif color_type == _color_types.color256:
        return '\x1b[48;5;{}m  '.format(_rgb_to_256(r, g, b, palette))
    elif color_type == _color_types.color16:
        escape_code_id = _rgb_to_16(r, g, b, palette)
        codepoint = None
        if escape_code_id >= 8:
            codepoint = '10' + str(escape_code_id - 8)
        else:
            codepoint = '4' + str(escape_code_id)
        return '\x1b[{}m  '.format(codepoint)
    elif color_type == _color_types.color8:
        escape_code_id = _rgb_to_8(r, g, b, palette)
        return '\x1b[4{}m  '.format(escape_code_id)
    else:
        raise ValueError("invalid color_type: {}".format(color_type))

# convert the two row's colors to a escape sequence (unicode does two rows at a time)
def _dual_pix_to_escape(r1, r2, g1, g2, b1, b2, color_type, palette):
    if color_type == _color_types.truecolor:
        return '\x1b[48;2;{};{};{}m\x1b[38;2;{};{};{}m▄'.format(r1, g1, b1, r2, g2, b2)
    elif color_type == _color_types.color256:
        return '\x1b[48;5;{}m\x1b[38;5;{}m▄'.format(_rgb_to_256(r1, g1, b1, palette), _rgb_to_256(r2, g2, b2, palette))
    elif color_type == _color_types.color16:
        bg_code_id = _rgb_to_16(r1, g1, b1, palette)
        fg_code_id = _rgb_to_16(r2, g2, b2, palette)
        bg_codepoint = None
        fg_codepoint = None
        if bg_code_id >= 8:
            bg_codepoint = '10' + str(bg_codepoint - 8)
        else:
            bg_codepoint = '4' + str(bg_codepoint)
        if fg_codepoint >= 8:
            fg_codepoint = '9' + str(fg_codepoint - 8)
        else:
            fg_codepoint = '3' + str(fg_codepoint)
        return '\x1b[{}m\x1b[{}m▄'.format(bg_codepoint, fg_codepoint)
    elif color_type == _color_types.color8:
        bg_code_id = _rgb_to_8(r1, g1, b1, palette)
        fg_code_id = _rgb_to_8(r2, g2, b2, palette)
        return '\x1b[4{}m\x1b[3{}m▄'.format(bg_code_id, fg_code_id)
    else:
        raise ValueError("invalid color_type: {}".format(color_type))

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
    ansi_string = ''

    yit = iter(range(destHeight))
    for y in yit:
        for x in range(destWidth):
            r, g, b = map(str, img.getpixel((x, y)))
            if is_unicode:
                # the next row's pixel
                rprime, gprime, bprime = map(str, img.getpixel((x, y+1)))
                ansi_string += _dual_pix_to_escape(r, rprime, g, gprime, b, bprime, color_type, palette)
            else:
                ansi_string += _pix_to_escape(r, g, b, color_type, palette)
        # line ending, reset colours
        ansi_string += '\x1b[0m\n'
        if is_unicode:
            # skip a row because we do two rows at once
            next(yit, None)

    return ansi_string