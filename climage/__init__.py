""" CLImage entry point """

import pkg_resources

__author__ = "Patrick Nappa"
__email__ = "patricknappa@gmail.com"
__version__ = pkg_resources.get_distribution('climage').version

from climage.main import main

if __name__ == "__main__":
    main()
