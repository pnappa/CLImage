
# python pseudo-port of https://github.com/dom111/image-to-ansi

colour_mapping = []

def _rgb_to_256(r, g, b):
    # TODO: i reckon I can replace this with a fast voronoi version
    # i.e. generate voronoi boundaries offline, then find which
    # bound the point is in.
    # TODO: as it is, this is rather slow actually!
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
                    colour_mapping.append([r1, g1, b1, 16 + int(
                                                str(int(5 * r1 // 255)) + 
                                                str(int(5 * g1 // 255)) +
                                                str(int(5 * b1 // 255)), 6)])

        for s in [8, 18, 28, 38, 48, 58, 68, 78, 88, 98, 108, 118, 128, 138, 148, 158, 168, 178, 188, 198, 208, 218, 228, 238]:
            colour_mapping.append([s, s, s, 232 + s // 10])

    if len(colour_mapping) == 0:
        gen_colours()

    r, g, b = map(int, (r, g, b))

    # get the best term colour
    def best(candidates, source):
        # based on the distance from the populated colour table - closest wins!
        return min(candidates, key=lambda x: abs(x[0] - source[0]) + 
                                             abs(x[1] - source[1]) + 
                                             abs(x[2] - source[2]))

    return best(colour_mapping, [r, g, b])[3]


# convert the rgb value into an escape sequence
def _pix_to_escape(r, g, b, is_truecolor):
    if is_truecolor:
        return '\x1b[48;2;{};{};{}m  '.format(r, g, b)
    else:
        return '\x1b[48;5;{}m  '.format(_rgb_to_256(r, g, b))

# convert the two row's colors to a escape sequence (unicode does two rows at a time)
def _dual_pix_to_escape(r1, r2, g1, g2, b1, b2, is_truecolor):
    if is_truecolor:
        return '\x1b[48;2;{};{};{}m\x1b[38;2;{};{};{}m▄'.format(r1, g1, b1, r2, g2, b2)
    else:
        return '\x1b[48;5;{}m\x1b[38;5;{}m▄'.format(_rgb_to_256(r1, g1, b1), _rgb_to_256(r2, g2, b2))

def _toAnsi(img, oWidth, is_unicode=False, is_truecolor=False):
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
                ansi_string += _dual_pix_to_escape(r, rprime, g, gprime, b, bprime, is_truecolor)
            else:
                ansi_string += _pix_to_escape(r, g, b, is_truecolor)
        # line ending, reset colours
        ansi_string += '\x1b[0m\n'
        if is_unicode:
            # skip a row because we do two rows at once
            next(yit, None)

    return ansi_string
