# -*- coding: utf-8 -*-
""" CLImage entry point """

import pkg_resources

__author__ = "Patrick Nappa"
__email__ = "patricknappa@gmail.com"
__version__ = pkg_resources.get_distribution('climage').version

from climage.__main__ import convert, to_file, main

if __name__ == "__main__":
    main()
