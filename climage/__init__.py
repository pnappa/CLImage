# -*- coding: utf-8 -*-
"""CLImage entry point"""

from .__version__ import __version__

__author__ = "Patrick Nappa"
__email__ = "patricknappa@gmail.com"

from climage.__main__ import (
    convert,
    to_file,
    main,
    convert_pil,
    convert_array,
    color_to_flags,
    get_ansi_pixel,
    get_reset_code,
    color_types,
    get_dual_unicode_ansi_pixels,
)

__all__: list[str] = [
    "__author__",
    "__email__",
    "convert",
    "to_file",
    "main",
    "convert_pil",
    "convert_array",
    "color_to_flags",
    "get_ansi_pixel",
    "get_reset_code",
    "color_types",
    "get_dual_unicode_ansi_pixels",
]

if __name__ == "__main__":
    main()
